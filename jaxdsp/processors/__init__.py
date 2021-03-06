from jaxdsp.processors import (
    allpass_filter,
    clip,
    delay_line,
    feedforward_delay,
    fir_filter,
    freeverb,
    iir_filter,
    lowpass_feedback_comb_filter,
    sine_wave,
)

all_processors = [
    allpass_filter,
    clip,
    delay_line,
    feedforward_delay,
    fir_filter,
    freeverb,
    iir_filter,
    lowpass_feedback_comb_filter,
    sine_wave,
]
processor_by_name = {processor.NAME: processor for processor in all_processors}
empty_carry = {"state": None, "params": None}


def is_nested_processor(processor):
    return processor.NAME == "Serial Processors"


def default_param_values(processor, processor_state=None):
    if is_nested_processor(processor):
        return {
            processor_name: default_param_values(processor_by_name[processor_name])
            for processor_name in processor_state.keys()
        }
    return {param.name: param.default_value for param in processor.PARAMS}


def serialize_processor(processor, params=None):
    if not processor:
        return None

    if is_nested_processor(processor) and params:
        return [serialize_processor(processor_by_name[inner_name], inner_params) for inner_name, inner_params in params.items()]

    return {
        "name": processor.NAME,
        "param_definitions": [param.serialize() for param in processor.PARAMS],
        "presets": processor.PRESETS,
        "params": params or default_param_values(processor),
    }


def param_by_name(processor_name):
    processor = processor_by_name.get(processor_name)
    return {param.name: param for param in processor.PARAMS} if processor else {}


def params_to_unit_scale(params, processor_name):
    return {
        name: params_to_unit_scale(value, name)
        if name in processor_by_name
        else param_by_name(processor_name)[name].to_unit_scale(value)
        for name, value in params.items()
    }


def params_from_unit_scale(params, processor_name):
    return {
        name: params_from_unit_scale(value, name)
        if name in processor_by_name
        else param_by_name(processor_name)[name].from_unit_scale(value)
        for name, value in params.items()
    }
