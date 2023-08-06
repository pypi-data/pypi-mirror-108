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
"""Tests for tink.python.tink.jwt._jwt_validator."""

import datetime

from absl.testing import absltest
from tink import jwt
from tink.jwt import _jwt_validator


class JwtValidatorTest(absltest.TestCase):

  def test_validator_getters(self):
    fixed_now = datetime.datetime.fromtimestamp(12345, datetime.timezone.utc)
    clock_skew = datetime.timedelta(minutes=1)
    validator = jwt.new_validator(
        issuer='issuer',
        subject='subject',
        audience='audience',
        fixed_now=fixed_now,
        clock_skew=clock_skew)
    self.assertTrue(validator.has_issuer())
    self.assertEqual(validator.issuer(), 'issuer')
    self.assertTrue(validator.has_subject())
    self.assertEqual(validator.subject(), 'subject')
    self.assertTrue(validator.has_audience())
    self.assertEqual(validator.audience(), 'audience')
    self.assertTrue(validator.has_fixed_now())
    self.assertEqual(validator.fixed_now(), fixed_now)
    self.assertEqual(validator.clock_skew(), clock_skew)

  def test_empty_validator_getters(self):
    validator = jwt.new_validator()
    self.assertFalse(validator.has_issuer())
    self.assertFalse(validator.has_subject())
    self.assertFalse(validator.has_audience())
    self.assertFalse(validator.has_fixed_now())
    self.assertFalse(validator.clock_skew(), datetime.timedelta())

  def test_too_much_clock_skew(self):
    with self.assertRaises(ValueError):
      jwt.new_validator(clock_skew=datetime.timedelta(minutes=20))

  def test_validate_expired_fails(self):
    expired = (datetime.datetime.now(tz=datetime.timezone.utc)
               - datetime.timedelta(minutes=1))
    token = jwt.new_raw_jwt(expiration=expired)
    validator = jwt.new_validator()
    with self.assertRaises(jwt.JwtInvalidError):
      _jwt_validator.validate(validator, token)

  def test_validate_not_expired_success(self):
    still_valid = (datetime.datetime.now(tz=datetime.timezone.utc)
                   + datetime.timedelta(minutes=1))
    token = jwt.new_raw_jwt(expiration=still_valid)
    validator = jwt.new_validator()
    _jwt_validator.validate(validator, token)

  def test_validate_token_that_expires_now_fails(self):
    now = datetime.datetime.fromtimestamp(1234.0, tz=datetime.timezone.utc)
    token = jwt.new_raw_jwt(expiration=now)
    validator = jwt.new_validator()
    with self.assertRaises(jwt.JwtInvalidError):
      _jwt_validator.validate(validator, token)

  def test_validate_recently_expired_with_clock_skew_success(self):
    recently_expired = (datetime.datetime.now(tz=datetime.timezone.utc)
                        - datetime.timedelta(minutes=1))
    token = jwt.new_raw_jwt(expiration=recently_expired)
    validator = jwt.new_validator(clock_skew=datetime.timedelta(minutes=2))
    # because of clock_skew, the recently expired token is valid
    _jwt_validator.validate(validator, token)

  def test_validate_not_before_in_the_future_fails(self):
    in_the_future = (datetime.datetime.now(tz=datetime.timezone.utc)
                     + datetime.timedelta(minutes=1))
    token = jwt.new_raw_jwt(not_before=in_the_future)
    validator = jwt.new_validator()
    with self.assertRaises(jwt.JwtInvalidError):
      _jwt_validator.validate(validator, token)

  def test_validate_not_before_in_the_past_success(self):
    in_the_past = (datetime.datetime.now(tz=datetime.timezone.utc)
                   - datetime.timedelta(minutes=1))
    token = jwt.new_raw_jwt(not_before=in_the_past)
    validator = jwt.new_validator()
    _jwt_validator.validate(validator, token)

  def test_validate_not_before_is_now_success(self):
    now = datetime.datetime.fromtimestamp(12345, datetime.timezone.utc)
    token = jwt.new_raw_jwt(not_before=now)
    validator = jwt.new_validator()
    _jwt_validator.validate(validator, token)

  def test_validate_not_before_almost_reached_with_clock_skew_success(self):
    in_one_minute = (datetime.datetime.now(tz=datetime.timezone.utc)
                     + datetime.timedelta(minutes=1))
    token = jwt.new_raw_jwt(not_before=in_one_minute)
    validator = jwt.new_validator(clock_skew=datetime.timedelta(minutes=2))
    _jwt_validator.validate(validator, token)

  def test_requires_issuer_but_no_issuer_set_fails(self):
    token = jwt.new_raw_jwt()
    validator = jwt.new_validator(issuer='issuer')
    with self.assertRaises(jwt.JwtInvalidError):
      _jwt_validator.validate(validator, token)

  def test_invalid_issuer_fails(self):
    token = jwt.new_raw_jwt(issuer='unknown')
    validator = jwt.new_validator(issuer='issuer')
    with self.assertRaises(jwt.JwtInvalidError):
      _jwt_validator.validate(validator, token)

  def test_correct_issuer_success(self):
    token = jwt.new_raw_jwt(issuer='issuer')
    validator = jwt.new_validator(issuer='issuer')
    _jwt_validator.validate(validator, token)

  def test_dont_check_issuer_success(self):
    validator = jwt.new_validator()
    token_without_issuer = jwt.new_raw_jwt()
    _jwt_validator.validate(validator, token_without_issuer)
    token_with_issuer = jwt.new_raw_jwt(issuer='issuer')
    _jwt_validator.validate(validator, token_with_issuer)

  def test_requires_subject_but_no_subject_set_fails(self):
    token = jwt.new_raw_jwt()
    validator = jwt.new_validator(subject='subject')
    with self.assertRaises(jwt.JwtInvalidError):
      _jwt_validator.validate(validator, token)

  def test_invalid_subject_fails(self):
    token = jwt.new_raw_jwt(subject='unknown')
    validator = jwt.new_validator(subject='subject')
    with self.assertRaises(jwt.JwtInvalidError):
      _jwt_validator.validate(validator, token)

  def test_correct_subject_success(self):
    token = jwt.new_raw_jwt(subject='subject')
    validator = jwt.new_validator(subject='subject')
    _jwt_validator.validate(validator, token)

  def test_dont_check_subject_success(self):
    validator = jwt.new_validator()
    token_without_subject = jwt.new_raw_jwt()
    _jwt_validator.validate(validator, token_without_subject)
    token_with_subject = jwt.new_raw_jwt(subject='subject')
    _jwt_validator.validate(validator, token_with_subject)

  def test_requires_audience_but_no_audience_set_fails(self):
    token = jwt.new_raw_jwt()
    validator = jwt.new_validator(audience='audience')
    with self.assertRaises(jwt.JwtInvalidError):
      _jwt_validator.validate(validator, token)

  def test_wrong_audience_fails(self):
    token = jwt.new_raw_jwt(audiences=['unknown'])
    validator = jwt.new_validator(audience='audience')
    with self.assertRaises(jwt.JwtInvalidError):
      _jwt_validator.validate(validator, token)

  def test_correct_audience_success(self):
    token = jwt.new_raw_jwt(audiences=['you', 'me'])
    validator = jwt.new_validator(audience='me')
    _jwt_validator.validate(validator, token)

  def test_audience_in_token_but_not_in_validator_fails(self):
    validator = jwt.new_validator()
    token_with_audience = jwt.new_raw_jwt(audiences=['audience'])
    with self.assertRaises(jwt.JwtInvalidError):
      _jwt_validator.validate(validator, token_with_audience)

  def test_no_audience_success(self):
    validator = jwt.new_validator()
    token = jwt.new_raw_jwt()
    _jwt_validator.validate(validator, token)

  def test_validate_with_fixed_now_expired_fails(self):
    in_two_minutes = (
        datetime.datetime.now(tz=datetime.timezone.utc) +
        datetime.timedelta(minutes=2))
    in_one_minute = in_two_minutes - datetime.timedelta(minutes=1)
    token = jwt.new_raw_jwt(expiration=in_one_minute)
    validator = jwt.new_validator(fixed_now=in_two_minutes)
    with self.assertRaises(jwt.JwtInvalidError):
      _jwt_validator.validate(validator, token)

  def test_validate_with_fixed_now_not_yet_valid_fails(self):
    two_minutes_ago = (
        datetime.datetime.now(tz=datetime.timezone.utc) -
        datetime.timedelta(minutes=2))
    one_minute_ago = two_minutes_ago + datetime.timedelta(minutes=1)
    token = jwt.new_raw_jwt(not_before=one_minute_ago)
    validator = jwt.new_validator(fixed_now=two_minutes_ago)
    with self.assertRaises(jwt.JwtInvalidError):
      _jwt_validator.validate(validator, token)

  def test_validate_with_fixed_now_valid_success(self):
    fixed_now = datetime.datetime.fromtimestamp(12345, datetime.timezone.utc)
    validator = jwt.new_validator(fixed_now=fixed_now)
    expiration = fixed_now + datetime.timedelta(minutes=1)
    not_before = fixed_now - datetime.timedelta(minutes=1)
    token = jwt.new_raw_jwt(expiration=expiration, not_before=not_before)
    _jwt_validator.validate(validator, token)

if __name__ == '__main__':
  absltest.main()
