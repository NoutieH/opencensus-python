# Copyright 2017, OpenCensus Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from opencensus.trace import print_exporter, samplers
from opencensus.trace.propagation import trace_context_http_header_format

DEFAULT_PYRAMID_TRACER_CONFIG = {
    'SAMPLER': samplers.AlwaysOnSampler(),
    'EXPORTER': print_exporter.PrintExporter(),
    'PROPAGATOR': trace_context_http_header_format.TraceContextPropagator(),
    # https://cloud.google.com/appengine/docs/flexible/python/
    # how-instances-are-managed#health_checking
    'BLACKLIST_PATHS': ['_ah/health'],
}


class PyramidTraceSettings(object):
    def __init__(self, registry):
        self.settings = registry.settings.get('OPENCENSUS', {})
        self.settings = self.settings.get(
            'TRACE', DEFAULT_PYRAMID_TRACER_CONFIG)

        _set_default_configs(self.settings, DEFAULT_PYRAMID_TRACER_CONFIG)

    def __getattr__(self, attr):
        # If not in defaults, it is something we cannot parse.
        if attr not in DEFAULT_PYRAMID_TRACER_CONFIG:
            raise AttributeError('Attribute {} does not exist.'.format(attr))

        return self.settings[attr]


def _set_default_configs(user_settings, default):
    """Set the default value to user settings if user not specified
    the value.
    """
    for key in default:
        if key not in user_settings:
            user_settings[key] = default[key]

    return user_settings
