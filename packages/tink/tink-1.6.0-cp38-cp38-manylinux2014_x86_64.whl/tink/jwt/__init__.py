# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Jwt package."""
from __future__ import absolute_import
from __future__ import division
# Placeholder for import for type annotations
from __future__ import print_function

import datetime
from typing import Dict, List, Mapping, Optional, Text, Union, cast

from tink.jwt import _jwt_error
from tink.jwt import _jwt_hmac_key_manager
from tink.jwt import _jwt_key_templates
from tink.jwt import _jwt_mac
from tink.jwt import _jwt_mac_wrapper
from tink.jwt import _jwt_public_key_sign
from tink.jwt import _jwt_public_key_verify
from tink.jwt import _jwt_validator
from tink.jwt import _raw_jwt
from tink.jwt import _verified_jwt

JwtInvalidError = _jwt_error.JwtInvalidError
RawJwt = _raw_jwt.RawJwt
VerifiedJwt = _verified_jwt.VerifiedJwt
JwtValidator = _jwt_validator.JwtValidator
Claim = _raw_jwt.Claim
JwtMac = _jwt_mac.JwtMac
JwtPublicKeySign = _jwt_public_key_sign.JwtPublicKeySign
JwtPublicKeyVerify = _jwt_public_key_verify.JwtPublicKeyVerify


def raw_jwt_from_json_payload(payload: Text) -> RawJwt:
  return _raw_jwt.RawJwt.from_json_payload(payload)


def new_raw_jwt(issuer: Optional[Text] = None,
                subject: Optional[Text] = None,
                audiences: Optional[List[Text]] = None,
                jwt_id: Optional[Text] = None,
                expiration: Optional[datetime.datetime] = None,
                not_before: Optional[datetime.datetime] = None,
                issued_at: Optional[datetime.datetime] = None,
                custom_claims: Mapping[Text, Claim] = None) -> RawJwt:
  return _raw_jwt.RawJwt.create(issuer, subject, audiences, jwt_id, expiration,
                                not_before, issued_at, custom_claims)


def new_validator(issuer: Optional[Text] = None,
                  subject: Optional[Text] = None,
                  audience: Optional[Text] = None,
                  clock_skew: Optional[datetime.timedelta] = None,
                  fixed_now: Optional[datetime.datetime] = None
                  ) -> JwtValidator:
  return JwtValidator(issuer, subject, audience, clock_skew, fixed_now)


jwt_hs256_template = _jwt_key_templates.jwt_hs256_template
jwt_hs384_template = _jwt_key_templates.jwt_hs384_template
jwt_hs512_template = _jwt_key_templates.jwt_hs512_template
jwt_es256_template = _jwt_key_templates.jwt_es256_template
jwt_es384_template = _jwt_key_templates.jwt_es384_template
jwt_es512_template = _jwt_key_templates.jwt_es512_template
jwt_rs256_2048_f4_template = _jwt_key_templates.jwt_rs256_2048_f4_template
jwt_rs256_3072_f4_template = _jwt_key_templates.jwt_rs256_3072_f4_template
jwt_rs384_3072_f4_template = _jwt_key_templates.jwt_rs384_3072_f4_template
jwt_rs512_4096_f4_template = _jwt_key_templates.jwt_rs512_4096_f4_template
jwt_ps256_2048_f4_template = _jwt_key_templates.jwt_ps256_2048_f4_template
jwt_ps256_3072_f4_template = _jwt_key_templates.jwt_ps256_3072_f4_template
jwt_ps384_3072_f4_template = _jwt_key_templates.jwt_ps384_3072_f4_template
jwt_ps512_4096_f4_template = _jwt_key_templates.jwt_ps512_4096_f4_template


def register_jwt_mac() -> None:
  _jwt_hmac_key_manager.register()
  _jwt_mac_wrapper.register()
