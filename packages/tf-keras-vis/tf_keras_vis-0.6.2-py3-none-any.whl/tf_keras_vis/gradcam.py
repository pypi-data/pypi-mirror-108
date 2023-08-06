import warnings

import numpy as np
import tensorflow as tf
import tensorflow.keras.backend as K
from packaging.version import parse as version
from scipy.ndimage.interpolation import zoom
from tensorflow.python.keras.layers.convolutional import Conv

from tf_keras_vis import ModelVisualization
from tf_keras_vis.utils import (find_layer, is_mixed_precision, standardize, zoom_factor)

if version(tf.version.VERSION) >= version("2.4.0"):
    from tensorflow.keras.mixed_precision import LossScaleOptimizer


class Gradcam(ModelVisualization):
    def __call__(
            self,
            score,
            seed_input,
            penultimate_layer=-1,
            seek_penultimate_conv_layer=True,
            activation_modifier=lambda cam: K.relu(cam),
            training=False,
            normalize_gradient=None,  # Disabled option.
            expand_cam=True,
            standardize_cam=True,
            unconnected_gradients=tf.UnconnectedGradients.NONE):
        """Generate gradient based class activation maps (CAM) by using positive gradient of
            penultimate_layer with respect to score.

            For details on Grad-CAM, see the paper:
            [Grad-CAM: Why did you say that? Visual Explanations from Deep Networks via
            Gradient-based Localization](https://arxiv.org/pdf/1610.02391v1.pdf).

        # Arguments
            score: A score function. If the model has multiple outputs, you can use a different
                score function on each output by passing a list of score functions.
            seed_input: An N-dim Numpy array. If the model has multiple inputs,
                you have to pass a list of N-dim Numpy arrays.
            penultimate_layer: A number of integer or a tf.keras.layers.Layer object.
            seek_penultimate_conv_layer: True to seek the penultimate layter that is a subtype of
                `keras.layers.convolutional.Conv` class.
                If False, the penultimate layer is that was elected by penultimate_layer index.
            activation_modifier: A function to modify gradients.
            normalize_gradient: Note! This option is now disabled.
            expand_cam: True to expand cam to same as input image size.
                ![Note] Even if the model has multiple inputs, this function return only one cam
                value (That's, when `expand_cam` is True, multiple cam images are generated from
                a model that has multiple inputs).
            training: A bool whether the model's trainig-mode turn on or off.
            standardize_cam: A bool. If True(default), cam will be standardized.
            unconnected_gradients: Specifies the gradient value returned when the given input
                tensors are unconnected. Accepted values are constants defined in the class
                `tf.UnconnectedGradients` and the default value is NONE.
        # Returns
            The heatmap image or a list of their images that indicate the `seed_input` regions
                whose change would most contribute  the score value,
        # Raises
            ValueError: In case of invalid arguments for `score`, or `penultimate_layer`.
        """
        if normalize_gradient is not None:
            warnings.warn(('`normalize_gradient` option of GradCAM#__call__() is disabled.,'
                           ' And this will be removed in future.'), DeprecationWarning)
        # Preparing
        scores = self._get_scores_for_multiple_outputs(score)
        seed_inputs = self._get_seed_inputs_for_multiple_inputs(seed_input)
        penultimate_output_tensor = self._find_penultimate_output(penultimate_layer,
                                                                  seek_penultimate_conv_layer)
        # Processing gradcam
        model = tf.keras.Model(inputs=self.model.inputs,
                               outputs=self.model.outputs + [penultimate_output_tensor])

        # When mixed precision enabled
        mixed_precision_model = is_mixed_precision(model)
        if mixed_precision_model:
            optimizer = LossScaleOptimizer(tf.keras.optimizers.RMSprop())

        with tf.GradientTape(watch_accessed_variables=False) as tape:
            tape.watch(seed_inputs)
            outputs = model(seed_inputs, training=training)
            outputs, penultimate_output = outputs[:-1], outputs[-1]
            score_values = self._calculate_scores(outputs, scores)
            if mixed_precision_model:
                score_values = [
                    optimizer.get_scaled_loss(score_value) for score_value in score_values
                ]
        grads = tape.gradient(score_values,
                              penultimate_output,
                              unconnected_gradients=unconnected_gradients)

        if mixed_precision_model:
            grads = optimizer.get_unscaled_gradients(grads)
            grads = tf.cast(grads, dtype=model.variable_dtype)
            penultimate_output = tf.cast(penultimate_output, dtype=model.variable_dtype)
            score_values = [tf.cast(v, dtype=model.variable_dtype) for v in score_values]

        weights = K.mean(grads, axis=tuple(range(grads.ndim)[1:-1]), keepdims=True)
        cam = np.sum(penultimate_output * weights, axis=-1)
        if activation_modifier is not None:
            cam = activation_modifier(cam)

        if not expand_cam:
            if standardize_cam:
                cam = standardize(cam)
            return cam

        # Visualizing
        factors = (zoom_factor(cam.shape, X.shape) for X in seed_inputs)
        cam = [zoom(cam, factor) for factor in factors]
        if standardize_cam:
            cam = [standardize(x) for x in cam]
        if len(self.model.inputs) == 1 and not isinstance(seed_input, list):
            cam = cam[0]
        return cam

    def _find_penultimate_output(self, layer, seek_conv_layer):
        _layer = layer
        if not isinstance(_layer, tf.keras.layers.Layer):
            if _layer is None:
                _layer = -1
            if isinstance(_layer, int) and _layer < len(self.model.layers):
                _layer = self.model.layers[int(_layer)]
            elif isinstance(_layer, str):
                _layer = find_layer(self.model, lambda l: l.name == _layer)
            else:
                raise ValueError('Invalid argument. `penultimate_layer`=', layer)
        if _layer is not None and seek_conv_layer:
            _layer = find_layer(self.model, lambda l: isinstance(l, Conv), offset=_layer)
        if _layer is None:
            raise ValueError(('Unable to determine penultimate `Conv` layer. '
                              '`penultimate_layer`='), layer)
        output = _layer.output
        if len(output.shape) < 3:
            raise ValueError(("Penultimate layer's output tensor MUST have "
                              "samples, spaces and channels dimensions. [{}]").format(output.shape))
        return output


class GradcamPlusPlus(Gradcam):
    def __call__(self,
                 score,
                 seed_input,
                 penultimate_layer=-1,
                 seek_penultimate_conv_layer=True,
                 activation_modifier=lambda cam: K.relu(cam),
                 expand_cam=True,
                 training=False,
                 standardize_cam=True,
                 unconnected_gradients=tf.UnconnectedGradients.NONE):
        """Generate gradient based class activation maps (CAM) by using positive gradient of
            penultimate_layer with respect to score.

            For details on GradCAM++, see the paper:
            [GradCAM++: Improved Visual Explanations for Deep Convolutional Networks]
            (https://arxiv.org/pdf/1710.11063.pdf).

        # Arguments
            score: A score function. If the model has multiple outputs, you can use a different
                score function on each output by passing a list of score functions.
            seed_input: An N-dim Numpy array. If the model has multiple inputs,
                you have to pass a list of N-dim Numpy arrays.
            penultimate_layer: A number of integer or a tf.keras.layers.Layer object.
            seek_penultimate_conv_layer: True to seek the penultimate layter that is a subtype of
                `keras.layers.convolutional.Conv` class.
                If False, the penultimate layer is that was elected by penultimate_layer index.
            activation_modifier: A function to modify gradients.
            expand_cam: True to expand cam to same as input image size.
                ![Note] Even if the model has multiple inputs, this function return only one cam
                value (That's, when `expand_cam` is True, multiple cam images are generated from
                a model that has multiple inputs).
            training: A bool whether the model's trainig-mode turn on or off.
            standardize_cam: A bool. If True(default), cam will be standardized.
            unconnected_gradients: Specifies the gradient value returned when the given input
                tensors are unconnected. Accepted values are constants defined in the class
                `tf.UnconnectedGradients` and the default value is NONE.
        # Returns
            The heatmap image or a list of their images that indicate the `seed_input` regions
                whose change would most contribute  the score value,
        # Raises
            ValueError: In case of invalid arguments for `score`, or `penultimate_layer`.
        """
        # Preparing
        scores = self._get_scores_for_multiple_outputs(score)
        seed_inputs = self._get_seed_inputs_for_multiple_inputs(seed_input)
        penultimate_output_tensor = self._find_penultimate_output(penultimate_layer,
                                                                  seek_penultimate_conv_layer)

        # Processing gradcam
        model = tf.keras.Model(inputs=self.model.inputs,
                               outputs=self.model.outputs + [penultimate_output_tensor])
        # When mixed precision enabled
        mixed_precision_enabled = is_mixed_precision(model)
        if mixed_precision_enabled:
            optimizer = LossScaleOptimizer(tf.keras.optimizers.RMSprop())

        with tf.GradientTape(watch_accessed_variables=False) as tape:
            tape.watch(seed_inputs)
            outputs = model(seed_inputs, training=training)
            outputs, penultimate_output = outputs[:-1], outputs[-1]
            score_values = self._calculate_scores(outputs, scores)
            if mixed_precision_enabled:
                score_values = [
                    optimizer.get_scaled_loss(score_value) for score_value in score_values
                ]
        grads = tape.gradient(score_values,
                              penultimate_output,
                              unconnected_gradients=unconnected_gradients)

        if is_mixed_precision(model):
            grads = optimizer.get_unscaled_gradients(grads)
            grads = tf.cast(grads, dtype=model.variable_dtype)
            penultimate_output = tf.cast(penultimate_output, dtype=model.variable_dtype)
            score_values = [tf.cast(v, dtype=model.variable_dtype) for v in score_values]

        score = sum([tf.math.exp(tf.reshape(v, (-1, ))) for v in score_values])
        score_shape = (-1, ) + tuple(np.ones(grads.ndim - 1, np.int))
        score = tf.reshape(score, score_shape)

        first_derivative = score * grads
        second_derivative = first_derivative * grads
        third_derivative = second_derivative * grads

        global_sum = K.sum(penultimate_output,
                           axis=tuple(np.arange(len(penultimate_output.shape))[1:-1]),
                           keepdims=True)

        alpha_denom = second_derivative * 2.0 + third_derivative * global_sum
        alpha_denom = alpha_denom + tf.cast((second_derivative == 0.0), second_derivative.dtype)
        alphas = second_derivative / alpha_denom

        alpha_normalization_constant = K.sum(alphas,
                                             axis=tuple(np.arange(len(alphas.shape))[1:-1]),
                                             keepdims=True)
        alpha_normalization_constant = alpha_normalization_constant + tf.cast(
            (alpha_normalization_constant == 0.0), alpha_normalization_constant.dtype)
        alphas = alphas / alpha_normalization_constant

        if activation_modifier is None:
            weights = first_derivative
        else:
            weights = activation_modifier(first_derivative)
        deep_linearization_weights = weights * alphas
        deep_linearization_weights = K.sum(
            deep_linearization_weights,
            axis=tuple(np.arange(len(deep_linearization_weights.shape))[1:-1]),
            keepdims=True)

        cam = K.sum(deep_linearization_weights * penultimate_output, axis=-1)
        if activation_modifier is not None:
            cam = activation_modifier(cam)

        if not expand_cam:
            if standardize_cam:
                cam = standardize(cam)
            return cam

        # Visualizing
        factors = (zoom_factor(cam.shape, X.shape) for X in seed_inputs)
        cam = [zoom(cam, factor) for factor in factors]
        if standardize_cam:
            cam = [standardize(x) for x in cam]
        if len(self.model.inputs) == 1 and not isinstance(seed_input, list):
            cam = cam[0]
        return cam
