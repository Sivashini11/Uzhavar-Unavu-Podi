import razorpay

client = razorpay.Client(
    auth=(
        "rzp_live_TEFImfUGcLzBQ7",
        "hGmzCpNm45Ff5wVHMFbezvfx"
    )
)

try:
    print(client.order.all())
    print("✅ Authentication Successful")
except Exception as e:
    print("❌ Authentication Failed")
    print(e)