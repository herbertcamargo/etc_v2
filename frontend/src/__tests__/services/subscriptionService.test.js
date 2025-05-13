import axios from 'axios';
import * as subscriptionService from '../../services/subscriptionService';

// Mock the axios module
jest.mock('axios');

describe('Subscription Service', () => {
  afterEach(() => {
    jest.clearAllMocks();
  });

  test('getSubscriptionPlans returns plan data', async () => {
    // Mock API response
    const mockPlans = [
      {
        id: 'price_monthly',
        name: 'Monthly Plan',
        price: 4.99
      },
      {
        id: 'price_yearly',
        name: 'Yearly Plan',
        price: 47.88
      }
    ];
    
    // Setup the mock axios response
    axios.get.mockResolvedValueOnce({ data: mockPlans });
    
    // Call the service
    const result = await subscriptionService.getSubscriptionPlans();
    
    // Verify axios was called correctly
    expect(axios.get).toHaveBeenCalledWith('/subscriptions/plans');
    
    // Verify the result is what we expect
    expect(result.data).toEqual(mockPlans);
  });

  test('getCurrentSubscription returns subscription when found', async () => {
    // Mock API response
    const mockSubscription = {
      id: 'sub_123',
      status: 'active',
      plan_type: 'month'
    };
    
    // Setup the mock axios response
    axios.get.mockResolvedValueOnce({ data: mockSubscription });
    
    // Call the service
    const result = await subscriptionService.getCurrentSubscription();
    
    // Verify axios was called correctly
    expect(axios.get).toHaveBeenCalledWith('/subscriptions/me');
    
    // Verify the result is what we expect
    expect(result.data).toEqual(mockSubscription);
  });

  test('getCurrentSubscription returns null for 404 response', async () => {
    // Setup the mock axios rejection
    const error = new Error('Not found');
    error.response = { status: 404 };
    axios.get.mockRejectedValueOnce(error);
    
    // Call the service
    const result = await subscriptionService.getCurrentSubscription();
    
    // Verify axios was called correctly
    expect(axios.get).toHaveBeenCalledWith('/subscriptions/me');
    
    // Verify the result is null
    expect(result.data).toBeNull();
  });

  test('getCurrentSubscription throws for non-404 errors', async () => {
    // Setup the mock axios rejection
    const error = new Error('Server error');
    error.response = { status: 500 };
    axios.get.mockRejectedValueOnce(error);
    
    // Call the service and expect it to throw
    await expect(subscriptionService.getCurrentSubscription()).rejects.toThrow();
    
    // Verify axios was called correctly
    expect(axios.get).toHaveBeenCalledWith('/subscriptions/me');
  });

  test('cancelSubscription calls the API correctly', async () => {
    // Setup the mock axios response
    axios.delete.mockResolvedValueOnce({ status: 204 });
    
    // Call the service
    await subscriptionService.cancelSubscription();
    
    // Verify axios was called correctly
    expect(axios.delete).toHaveBeenCalledWith('/subscriptions/me');
  });

  test('createCheckoutSession sends checkout data', async () => {
    // Mock checkout data
    const checkoutData = {
      price_id: 'price_monthly',
      success_url: 'http://example.com/success',
      cancel_url: 'http://example.com/cancel'
    };
    
    // Mock API response
    const mockResponse = {
      checkout_url: 'https://checkout.stripe.com/test',
      session_id: 'cs_test_123'
    };
    
    // Setup the mock axios response
    axios.post.mockResolvedValueOnce({ data: mockResponse });
    
    // Call the service
    const result = await subscriptionService.createCheckoutSession(checkoutData);
    
    // Verify axios was called correctly
    expect(axios.post).toHaveBeenCalledWith('/subscriptions/checkout', checkoutData);
    
    // Verify the result is what we expect
    expect(result.data).toEqual(mockResponse);
  });

  test('getSubscriptionUsage returns usage data', async () => {
    // Mock API response
    const mockUsage = {
      plan_type: 'free',
      transcriptions_used: 2,
      transcriptions_limit: 3,
      transcriptions_remaining: 1,
      is_limited: true
    };
    
    // Setup the mock axios response
    axios.get.mockResolvedValueOnce({ data: mockUsage });
    
    // Call the service
    const result = await subscriptionService.getSubscriptionUsage();
    
    // Verify axios was called correctly
    expect(axios.get).toHaveBeenCalledWith('/subscriptions/usage');
    
    // Verify the result is what we expect
    expect(result.data).toEqual(mockUsage);
  });
}); 