# Stripe Integration Guide

## Overview
This document provides essential information about integrating Stripe payment processing in server-side applications using Python and JavaScript SDKs. All AI agents should reference this guide when handling Stripe-related code or functionality.

## Installation

### Python
```python
pip install stripe
```

### JavaScript (Node.js)
```javascript
npm install stripe
```

## Authentication

### Python
```python
import stripe
stripe.api_key = "sk_test_..."  # Test key
# stripe.api_key = "sk_live_..."  # Production key
```

### JavaScript
```javascript
const stripe = require('stripe')('sk_test_...');  // Test key
// const stripe = require('stripe')('sk_live_...');  // Production key
```

## Core Concepts

### 1. API Keys
- **Secret API keys** (`sk_*`): Must be kept secure and used only on the server-side
- **Publishable keys** (`pk_*`): Can be safely used in client-side code
- **Test keys** (`sk_test_*` or `pk_test_*`): Use in development environments
- **Live keys** (`sk_live_*` or `pk_live_*`): Use in production environments
- **Restricted API keys**: Create with limited permissions for specific services

### 2. Idempotency
For non-idempotent requests, use idempotency keys to prevent duplicate operations:

#### Python
```python
stripe.Charge.create(
    amount=2000,
    currency="usd",
    source="tok_mastercard",
    idempotency_key="a-unique-key-for-this-specific-charge"
)
```

#### JavaScript
```javascript
stripe.charges.create(
    {
        amount: 2000,
        currency: 'usd',
        source: 'tok_mastercard',
    },
    {
        idempotencyKey: 'a-unique-key-for-this-specific-charge'
    }
);
```

### 3. Versioning
Specify the Stripe API version to ensure consistent behavior:

#### Python
```python
stripe.api_version = "2023-10-16"
```

#### JavaScript
```javascript
const stripe = require('stripe')('sk_test_...', {
    apiVersion: '2023-10-16',
});
```

## Common Operations

### Creating a Customer

#### Python
```python
customer = stripe.Customer.create(
    email="customer@example.com",
    name="Jenny Rosen",
    payment_method="pm_card_visa",
)
```

#### JavaScript
```javascript
const customer = await stripe.customers.create({
    email: 'customer@example.com',
    name: 'Jenny Rosen',
    payment_method: 'pm_card_visa',
});
```

### Creating a Payment Intent

#### Python
```python
intent = stripe.PaymentIntent.create(
    amount=1099,
    currency="usd",
    customer=customer.id,
    payment_method="pm_card_visa",
    off_session=True,
    confirm=True,
)
```

#### JavaScript
```javascript
const paymentIntent = await stripe.paymentIntents.create({
    amount: 1099,
    currency: 'usd',
    customer: customer.id,
    payment_method: 'pm_card_visa',
    off_session: true,
    confirm: true,
});
```

### Creating a Subscription

#### Python
```python
subscription = stripe.Subscription.create(
    customer=customer.id,
    items=[
        {"price": "price_12345"},
    ],
)
```

#### JavaScript
```javascript
const subscription = await stripe.subscriptions.create({
    customer: customer.id,
    items: [
        {price: 'price_12345'},
    ],
});
```

### Listing Resources

#### Python
```python
# List all customers, 10 at a time
customers = stripe.Customer.list(limit=10)

# Iterate through customers
for customer in customers.auto_paging_iter():
    print(customer.id)
```

#### JavaScript
```javascript
// List all customers, 10 at a time
const customers = await stripe.customers.list({
    limit: 10,
});

// Using for...of
for await (const customer of stripe.customers.list({limit: 3})) {
    console.log(customer.id);
}
```

## Handling Errors

### Python
```python
import stripe
try:
    # Use Stripe's library to make requests
    pass
except stripe.error.CardError as e:
    # Since it's a decline, stripe.error.CardError will be caught
    print(f"Status is: {e.http_status}")
    print(f"Code is: {e.code}")
    print(f"Message is: {e.user_message}")
except stripe.error.RateLimitError as e:
    # Too many requests made to the API too quickly
    pass
except stripe.error.InvalidRequestError as e:
    # Invalid parameters were supplied to Stripe's API
    pass
except stripe.error.AuthenticationError as e:
    # Authentication with Stripe's API failed
    # (maybe you changed API keys recently)
    pass
except stripe.error.APIConnectionError as e:
    # Network communication with Stripe failed
    pass
except stripe.error.StripeError as e:
    # Display a very generic error to the user
    pass
except Exception as e:
    # Something else happened, completely unrelated to Stripe
    pass
```

### JavaScript
```javascript
try {
    // Use Stripe's library to make requests
} catch (error) {
    if (error.type === 'StripeCardError') {
        // Display a very specific error message
        console.log(`Card error: ${error.message}`);
    } else if (error.type === 'StripeRateLimitError') {
        // Too many requests made to the API too quickly
        console.log('Rate limit error');
    } else if (error.type === 'StripeInvalidRequestError') {
        // Invalid parameters were supplied to Stripe's API
        console.log('Invalid request error');
    } else if (error.type === 'StripeAPIError') {
        // An error occurred internally with Stripe's API
        console.log('API error');
    } else if (error.type === 'StripeConnectionError') {
        // Some kind of error occurred during the HTTPS communication
        console.log('Connection error');
    } else if (error.type === 'StripeAuthenticationError') {
        // You probably used an incorrect API key
        console.log('Authentication error');
    } else {
        // Handle any other types of unexpected errors
        console.log('Other error occurred');
    }
}
```

## Webhooks

### Python
```python
@app.route('/webhook', methods=['POST'])
def webhook_received():
    webhook_secret = 'whsec_...'
    request_data = json.loads(request.data)

    if webhook_secret:
        # Retrieve the event by verifying the signature using the raw body and secret
        signature = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload=request.data, sig_header=signature, secret=webhook_secret)
            data = event['data']
        except Exception as e:
            return e
        # Get the type of webhook event sent
        event_type = event['type']
    else:
        data = request_data['data']
        event_type = request_data['type']
    
    # Handle the event
    if event_type == 'payment_intent.succeeded':
        payment_intent = data['object']
        # Handle payment_intent.succeeded event
    elif event_type == 'payment_method.attached':
        payment_method = data['object']
        # Handle payment_method.attached event
    # ... handle other event types
    else:
        print('Unhandled event type {}'.format(event_type))

    return jsonify({'status': 'success'})
```

### JavaScript
```javascript
// Using Express
const express = require('express');
const app = express();

// Match the raw body to content type application/json
app.post('/webhook', express.raw({type: 'application/json'}), (request, response) => {
    const sig = request.headers['stripe-signature'];
    const webhookSecret = 'whsec_...';

    let event;

    try {
        event = stripe.webhooks.constructEvent(request.body, sig, webhookSecret);
    } catch (err) {
        response.status(400).send(`Webhook Error: ${err.message}`);
        return;
    }

    // Handle the event
    switch (event.type) {
        case 'payment_intent.succeeded':
            const paymentIntent = event.data.object;
            // Handle payment_intent.succeeded event
            break;
        case 'payment_method.attached':
            const paymentMethod = event.data.object;
            // Handle payment_method.attached event
            break;
        // ... handle other event types
        default:
            console.log(`Unhandled event type ${event.type}`);
    }

    // Return a 200 response to acknowledge receipt of the event
    response.send();
});
```

## Best Practices

### Security
1. **Never log API keys** or other sensitive data
2. **Use webhook signatures** to verify webhook sources
3. **Implement TLS/HTTPS** for all communications
4. **Keep SDKs updated** to the latest version
5. **Use restricted API keys** with only necessary permissions

### Architecture
1. **Separate Stripe logic** into dedicated service modules
2. **Store Stripe customer IDs** with your user records
3. **Use idempotency keys** for non-GET requests
4. **Handle webhooks** for asynchronous event processing
5. **Implement proper error handling** for all Stripe operations

### Testing
1. **Use test API keys** for development and testing
2. **Leverage Stripe CLI** for local webhook testing
3. **Create test customers and cards** using test mode
4. **Test both successful and failed payments**
5. **Test webhooks** for reliability

## Common Patterns

### Save Card for Later
```python
# Python
payment_method = stripe.PaymentMethod.create(
    type="card",
    card={
        "number": "4242424242424242",
        "exp_month": 8,
        "exp_year": 2025,
        "cvc": "314",
    },
)

customer = stripe.Customer.create()
stripe.PaymentMethod.attach(
    payment_method.id,
    customer=customer.id,
)
```

```javascript
// JavaScript
const paymentMethod = await stripe.paymentMethods.create({
    type: 'card',
    card: {
        number: '4242424242424242',
        exp_month: 8,
        exp_year: 2025,
        cvc: '314',
    },
});

const customer = await stripe.customers.create();
await stripe.paymentMethods.attach(
    paymentMethod.id,
    {customer: customer.id}
);
```

### Subscription Management
```python
# Python
# Create a subscription
subscription = stripe.Subscription.create(
    customer=customer.id,
    items=[{"price": "price_12345"}],
    payment_behavior='default_incomplete',
    expand=['latest_invoice.payment_intent'],
)

# Update a subscription
updated_subscription = stripe.Subscription.modify(
    "sub_12345",
    items=[{
        "id": "si_12345",
        "price": "price_67890",
    }],
)

# Cancel a subscription
stripe.Subscription.delete("sub_12345")
```

```javascript
// JavaScript
// Create a subscription
const subscription = await stripe.subscriptions.create({
    customer: customer.id,
    items: [{price: 'price_12345'}],
    payment_behavior: 'default_incomplete',
    expand: ['latest_invoice.payment_intent'],
});

// Update a subscription
const updatedSubscription = await stripe.subscriptions.update(
    'sub_12345',
    {
        items: [{
            id: 'si_12345',
            price: 'price_67890',
        }],
    }
);

// Cancel a subscription
await stripe.subscriptions.del('sub_12345');
```

## Environment-Specific Considerations

### Development
- Use Stripe test API keys
- Install and use Stripe CLI for webhook testing
- Use test card numbers (e.g., 4242 4242 4242 4242)

### Production
- Switch to live API keys
- Implement comprehensive error handling
- Set up robust webhook handling
- Configure correct webhook URLs in Stripe Dashboard
- Monitor Stripe Dashboard for errors and disputes

## Resources
- [Stripe API Reference](https://stripe.com/docs/api)
- [Python SDK Documentation](https://stripe.com/docs/api?lang=python)
- [Node.js SDK Documentation](https://stripe.com/docs/api?lang=node)
- [Stripe Testing Documentation](https://stripe.com/docs/testing)
- [Stripe CLI](https://stripe.com/docs/stripe-cli)