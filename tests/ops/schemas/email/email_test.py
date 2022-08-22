from fidesops.ops.schemas.email.email import SubjectIdentityVerificationBodyParams




def test_get_verification_code_ttl_minutes_calc():
    model_1 = SubjectIdentityVerificationBodyParams(verification_code="123123", verification_code_ttl_seconds=600)
    assert model_1.get_verification_code_ttl_minutes() == 10

    model_2 = SubjectIdentityVerificationBodyParams(verification_code="123123", verification_code_ttl_seconds=155)
    assert model_2.get_verification_code_ttl_minutes() == 2

    model_3 = SubjectIdentityVerificationBodyParams(verification_code="123123", verification_code_ttl_seconds=33)
    assert model_3.get_verification_code_ttl_minutes() == 0



