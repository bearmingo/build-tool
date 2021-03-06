# Copyright 2015 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Configures devil for use in chromium."""

import os

from devil import devil_env


_DEVIL_CONFIG = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'devil_chromium.json'))

_DEVIL_BUILD_PRODUCT_DEPS = {
  'forwarder_device': [
    {
      'platform': 'android',
      'arch': 'armeabi-v7a',
      'name': 'forwarder_dist',
    },
    {
      'platform': 'android',
      'arch': 'arm64-v8a',
      'name': 'forwarder_dist',
    },
    {
      'platform': 'android',
      'arch': 'mips',
      'name': 'forwarder_dist',
    },
    {
      'platform': 'android',
      'arch': 'mips64',
      'name': 'forwarder_dist',
    },
    {
      'platform': 'android',
      'arch': 'x86',
      'name': 'forwarder_dist',
    },
    {
      'platform': 'android',
      'arch': 'x86_64',
      'name': 'forwarder_dist',
    },
  ],
  'forwarder_host': [
    {
      'platform': 'linux',
      'arch': 'x86_64',
      'name': 'host_forwarder',
    },
  ],
  'md5sum_device': [
    {
      'platform': 'android',
      'arch': 'armeabi-v7a',
      'name': 'md5sum_dist',
    },
    {
      'platform': 'android',
      'arch': 'arm64-v8a',
      'name': 'md5sum_dist',
    },
    {
      'platform': 'android',
      'arch': 'mips',
      'name': 'md5sum_dist',
    },
    {
      'platform': 'android',
      'arch': 'mips64',
      'name': 'md5sum_dist',
    },
    {
      'platform': 'android',
      'arch': 'x86',
      'name': 'md5sum_dist',
    },
    {
      'platform': 'android',
      'arch': 'x86_64',
      'name': 'md5sum_dist',
    },
  ],
  'md5sum_host': [
    {
      'platform': 'linux',
      'arch': 'x86_64',
      'name': 'md5sum_bin_host',
    },
  ],
}


def Initialize(output_directory=None, custom_deps=None):
  """Initializes devil with chromium's binaries and third-party libraries.

  This includes:
    - Libraries:
      - the android SDK ("android_sdk")
      - pymock ("pymock")
    - Build products:
      - host & device forwarder binaries
          ("forwarder_device" and "forwarder_host")
      - host & device md5sum binaries ("md5sum_device" and "md5sum_host")

  Args:
    output_directory: An optional path to the output directory. If not set,
      no built dependencies are configured.
    custom_deps: An optional dictionary specifying custom dependencies.
      This should be of the form:

        {
          'dependency_name': {
            'platform': 'path',
            ...
          },
          ...
        }
  """

  devil_dynamic_config = {
    'config_type': 'BaseConfig',
    'dependencies': {},
  }
  if output_directory:
    devil_dynamic_config['dependencies'] = {
      dep_name: {
        'file_info': {
          '%s_%s' % (dep_config['platform'], dep_config['arch']): {
            'local_paths': [
              os.path.join(output_directory, dep_config['name']),
            ],
          }
          for dep_config in dep_configs
        }
      }
      for dep_name, dep_configs in _DEVIL_BUILD_PRODUCT_DEPS.iteritems()
    }
  if custom_deps:
    devil_dynamic_config['dependencies'].update(custom_deps)

  devil_env.config.Initialize(
      configs=[devil_dynamic_config], config_files=[_DEVIL_CONFIG])

