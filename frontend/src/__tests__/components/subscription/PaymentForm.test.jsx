import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import PaymentForm from '../../../components/subscription/PaymentForm';
import { createCheckoutSession } from '../../../services/subscriptionService';

// Mock the subscription service
jest.mock('../../../services/subscriptionService', () => ({
  createCheckoutSession: jest.fn()
}));

// Mock window.location.href
const originalLocation = window.location;
delete window.location;
window.location = { href: '', origin: 'http://localhost:3000' };

describe('PaymentForm component', () => {
  const mockSelectedPlanId = 'price_monthly';
  const mockOnPaymentStart = jest.fn();
  const mockOnPaymentCancel = jest.fn();
  const mockOnError = jest.fn();
  
  beforeEach(() => {
    jest.clearAllMocks();
  });
  
  afterAll(() => {
    window.location = originalLocation;
  });

  test('renders correctly with selected plan', () => {
    render(
      <PaymentForm 
        selectedPlanId={mockSelectedPlanId}
        onPaymentStart={mockOnPaymentStart}
        onPaymentCancel={mockOnPaymentCancel}
        onError={mockOnError}
      />
    );
    
    // Check title and description
    expect(screen.getByText('Complete Your Subscription')).toBeInTheDocument();
    expect(screen.getByText(/You'll be redirected to Stripe/)).toBeInTheDocument();
    
    // Check security badge
    expect(screen.getByText('Secure Checkout with Stripe')).toBeInTheDocument();
    
    // Check buttons
    expect(screen.getByText('Proceed to Checkout')).toBeInTheDocument();
    expect(screen.getByText('Cancel')).toBeInTheDocument();
  });

  test('handles checkout button click correctly', async () => {
    // Mock successful checkout response
    createCheckoutSession.mockResolvedValueOnce({
      data: {
        checkout_url: 'https://checkout.stripe.com/test-checkout',
        session_id: 'cs_test_123'
      }
    });
    
    render(
      <PaymentForm 
        selectedPlanId={mockSelectedPlanId}
        onPaymentStart={mockOnPaymentStart}
        onPaymentCancel={mockOnPaymentCancel}
        onError={mockOnError}
      />
    );
    
    // Click checkout button
    fireEvent.click(screen.getByText('Proceed to Checkout'));
    
    // Check that onPaymentStart was called
    expect(mockOnPaymentStart).toHaveBeenCalled();
    
    // Check that createCheckoutSession was called with correct data
    expect(createCheckoutSession).toHaveBeenCalledWith({
      price_id: mockSelectedPlanId,
      success_url: 'http://localhost:3000/subscription/success',
      cancel_url: 'http://localhost:3000/subscription'
    });
    
    // Wait for redirect
    await waitFor(() => {
      expect(window.location.href).toBe('https://checkout.stripe.com/test-checkout');
    });
  });

  test('handles checkout error correctly', async () => {
    // Mock error response
    const mockError = new Error('Checkout failed');
    mockError.response = {
      data: {
        detail: 'Payment processing error'
      }
    };
    createCheckoutSession.mockRejectedValueOnce(mockError);
    
    render(
      <PaymentForm 
        selectedPlanId={mockSelectedPlanId}
        onPaymentStart={mockOnPaymentStart}
        onPaymentCancel={mockOnPaymentCancel}
        onError={mockOnError}
      />
    );
    
    // Click checkout button
    fireEvent.click(screen.getByText('Proceed to Checkout'));
    
    // Wait for error handling
    await waitFor(() => {
      expect(mockOnError).toHaveBeenCalledWith('Payment processing error');
    });
    
    // Check that window location was not changed
    expect(window.location.href).not.toBe('https://checkout.stripe.com/test-checkout');
  });

  test('handles cancel button click', () => {
    render(
      <PaymentForm 
        selectedPlanId={mockSelectedPlanId}
        onPaymentStart={mockOnPaymentStart}
        onPaymentCancel={mockOnPaymentCancel}
        onError={mockOnError}
      />
    );
    
    // Click cancel button
    fireEvent.click(screen.getByText('Cancel'));
    
    // Check that onPaymentCancel was called
    expect(mockOnPaymentCancel).toHaveBeenCalled();
  });

  test('disables checkout button when no plan selected', () => {
    render(
      <PaymentForm 
        selectedPlanId={null}
        onPaymentStart={mockOnPaymentStart}
        onPaymentCancel={mockOnPaymentCancel}
        onError={mockOnError}
      />
    );
    
    // Check that checkout button is disabled
    expect(screen.getByText('Proceed to Checkout')).toBeDisabled();
  });

  test('shows loading state while processing', async () => {
    // Mock delayed checkout response
    createCheckoutSession.mockImplementationOnce(() => new Promise(resolve => {
      setTimeout(() => {
        resolve({
          data: {
            checkout_url: 'https://checkout.stripe.com/test-checkout',
            session_id: 'cs_test_123'
          }
        });
      }, 100);
    }));
    
    render(
      <PaymentForm 
        selectedPlanId={mockSelectedPlanId}
        onPaymentStart={mockOnPaymentStart}
        onPaymentCancel={mockOnPaymentCancel}
        onError={mockOnError}
      />
    );
    
    // Click checkout button
    fireEvent.click(screen.getByText('Proceed to Checkout'));
    
    // Check that button shows processing state
    expect(screen.getByText('Processing...')).toBeInTheDocument();
    expect(screen.getByText('Processing...')).toBeDisabled();
  });
}); 