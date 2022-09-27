from utils import QuickstartBase


base = QuickstartBase()


for num in [45, 14, 9, 4]:
    # key = f"dsr_countdown_{num}"
    key = "download"
    base.create_policy(
        key=key,
        execution_timeframe=num,
    )
    base.create_access_request(policy_key=key)
