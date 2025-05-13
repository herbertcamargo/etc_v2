import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import SubscriptionPage from '../../pages/SubscriptionPage';
import * as subscriptionService from '../../services/subscriptionService';
import { useAuth } from '../../hooks/useAuth';

// Mock the subscription service
jest.mock('../../services/subscriptionService');

// Mock the auth hook
jest.mock('../../hooks/useAuth');

// Mock the Layout component
jest.mock('../../components/layout/Layout', () => {
  return ({ children }) => <div data-testid="layout">{children}</div>;
});

describe('SubscriptionPage component', () => {
  const mockUser = {
    id: 'user123',
    username: 'testuser',
    is_premium: false
  };
  
  const mockPlans = [
    {
      id: 'price_monthly',
      name: 'Monthly Plan',
      description: 'Monthly description',
      price: 4.99,
      currency: 'USD',
      interval: 'month',
      features: ['Feature 1', 'Feature 2']
    },
    {
      id: 'price_yearly',
      name: 'Yearly Plan',
      description: 'Yearly description',
      price: 47.88,
      currency: 'USD',
      interval: 'year',
      features: ['Feature 1', 'Feature 2', 'Feature 3']
    }
  ];
  
  const mockUsage = {
    plan_type: 'free',
    transcriptions_used: 1,
    transcriptions_limit: 3,
    transcriptions_remaining: 2,
    is_limited: true,
    renewal_date: null
  };
  
  // Setup default mocks
  beforeEach(() => {
    useAuth.mockReturnValue({
      user: mockUser,
      isAuthenticated: true
    });
    
    subscriptionService.getSubscriptionPlans.mockResolvedValue({ data: mockPlans });
    subscriptionService.getCurrentSubscription.mockResolvedValue({ data: null });
    subscriptionService.getSubscriptionUsage.mockResolvedValue({ data: mockUsage });
  });
  
  afterEach(() => {
    jest.clearAllMocks();
  });

  test('renders without subscription', async () => {
    render(
      <BrowserRouter>
        <SubscriptionPage />
      </BrowserRouter>
    );
    
    // Check loading initially
    expect(screen.getByText('Loading subscription data...')).toBeInTheDocument();
    
    // Wait for data to load
    await waitFor(() => {
      expect(screen.queryByText('Loading subscription data...')).not.toBeInTheDocument();
    });
    
    // Check subscription heading
    expect(screen.getByText('Subscription')).toBeInTheDocument();
    expect(screen.getByText('Choose a subscription plan to unlock unlimited transcriptions')).toBeInTheDocument();
    
    // Check plans are rendered
    expect(screen.getByText('Monthly Plan')).toBeInTheDocument();
    expect(screen.getByText('Yearly Plan')).toBeInTheDocument();
    
    // Check usage is rendered
    expect(screen.getByText('Free Tier')).toBeInTheDocument();
    expect(screen.getByText('Subscription Usage')).toBeInTheDocument();
  });

  test('renders with active subscription', async () => {
    const mockSubscription = {
      id: 'sub_123',
      plan_type: 'month',
      status: 'active',
      end_date: '2023-07-15T00:00:00.000Z'
    };
    
    const mockPremiumUsage = {
      ...mockUsage,
      plan_type: 'month',
      is_limited: false,
      transcriptions_limit: Infinity,
      transcriptions_remaining: Infinity,
      renewal_date: '2023-07-15T00:00:00.000Z'
    };
    
    subscriptionService.getCurrentSubscription.mockResolvedValue({ data: mockSubscription });
    subscriptionService.getSubscriptionUsage.mockResolvedValue({ data: mockPremiumUsage });
    
    render(
      <BrowserRouter>
        <SubscriptionPage />
      </BrowserRouter>
    );
    
    // Wait for data to load
    await waitFor(() => {
      expect(screen.queryByText('Loading subscription data...')).not.toBeInTheDocument();
    });
    
    // Check subscription heading
    expect(screen.getByText('Subscription')).toBeInTheDocument();
    expect(screen.getByText('Manage your subscription and usage')).toBeInTheDocument();
    
    // Check current subscription section is rendered
    expect(screen.getByText('Current Subscription')).toBeInTheDocument();
    expect(screen.getByText('Monthly Premium')).toBeInTheDocument();
    expect(screen.getByText('Active')).toBeInTheDocument();
    
    // Check cancel button is rendered
    expect(screen.getByText('Cancel Subscription')).toBeInTheDocument();
    
    // Plans should not be rendered
    expect(screen.queryByText('Available Plans')).not.toBeInTheDocument();
  });

  test('displays error message on load failure', async () => {
    subscriptionService.getSubscriptionPlans.mockRejectedValue(new Error('Failed to load plans'));
    
    render(
      <BrowserRouter>
        <SubscriptionPage />
      </BrowserRouter>
    );
    
    // Wait for error to appear
    await waitFor(() => {
      expect(screen.getByText('Failed to load subscription data. Please try again.')).toBeInTheDocument();
    });
    
    // Check dismiss button
    expect(screen.getByText('Dismiss')).toBeInTheDocument();
  });

  test('handles plan selection', async () => {
    render(
      <BrowserRouter>
        <SubscriptionPage />
      </BrowserRouter>
    );
    
    // Wait for data to load
    await waitFor(() => {
      expect(screen.queryByText('Loading subscription data...')).not.toBeInTheDocument();
    });
    
    // Select the monthly plan
    const selectButtons = screen.getAllByText('Select Plan');
    fireEvent.click(selectButtons[0]); // First plan button
    
    // Check payment form appears
    await waitFor(() => {
      expect(screen.getByText('Complete Your Subscription')).toBeInTheDocument();
    });
  });

  test('handles subscription cancellation', async () => {
    const mockSubscription = {
      id: 'sub_123',
      plan_type: 'month',
      status: 'active',
      end_date: '2023-07-15T00:00:00.000Z'
    };
    
    subscriptionService.getCurrentSubscription.mockResolvedValue({ data: mockSubscription });
    subscriptionService.cancelSubscription.mockResolvedValue({ status: 204 });
    
    // Mock window.confirm
    const originalConfirm = window.confirm;
    window.confirm = jest.fn(() => true);
    
    render(
      <BrowserRouter>
        <SubscriptionPage />
      </BrowserRouter>
    );
    
    // Wait for data to load
    await waitFor(() => {
      expect(screen.queryByText('Loading subscription data...')).not.toBeInTheDocument();
    });
    
    // Click cancel subscription button
    fireEvent.click(screen.getByText('Cancel Subscription'));
    
    // Check confirmation was shown
    expect(window.confirm).toHaveBeenCalled();
    
    // Check subscription service was called
    await waitFor(() => {
      expect(subscriptionService.cancelSubscription).toHaveBeenCalled();
    });
    
    // Restore original confirm
    window.confirm = originalConfirm;
  });
}); 