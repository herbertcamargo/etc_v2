import React from 'react';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import SubscriptionNotification from '../../../components/subscription/SubscriptionNotification';

describe('SubscriptionNotification component', () => {
  const renderWithRouter = (ui) => {
    return render(
      <BrowserRouter>
        {ui}
      </BrowserRouter>
    );
  };

  test('renders free plan badge correctly', () => {
    const freeUsage = {
      plan_type: 'free',
      transcriptions_used: 1,
      transcriptions_limit: 3,
      transcriptions_remaining: 2,
      is_limited: true,
      renewal_date: null
    };
    
    renderWithRouter(
      <SubscriptionNotification 
        usage={freeUsage} 
        subscription={null} 
      />
    );
    
    // Check badge text
    expect(screen.getByText('2 Left')).toBeInTheDocument();
    
    // Check badge class
    const badge = screen.getByText('2 Left').closest('.subscription-badge');
    expect(badge).toHaveClass('subscription-badge--free');
    
    // Check icon
    expect(badge.querySelector('.subscription-badge__icon')).toHaveTextContent('⚡');
  });

  test('renders premium badge correctly', () => {
    const premiumUsage = {
      plan_type: 'month',
      transcriptions_used: 10,
      transcriptions_limit: Infinity,
      transcriptions_remaining: Infinity,
      is_limited: false,
      renewal_date: '2023-07-15T00:00:00.000Z'
    };
    
    const subscription = {
      id: 'sub_123',
      plan_type: 'month',
      status: 'active'
    };
    
    renderWithRouter(
      <SubscriptionNotification 
        usage={premiumUsage} 
        subscription={subscription} 
      />
    );
    
    // Check badge text
    expect(screen.getByText('Premium')).toBeInTheDocument();
    
    // Check badge class
    const badge = screen.getByText('Premium').closest('.subscription-badge');
    expect(badge).toHaveClass('subscription-badge--premium');
    
    // Check icon
    expect(badge.querySelector('.subscription-badge__icon')).toHaveTextContent('★');
  });

  test('renders yearly premium badge correctly', () => {
    const yearlyUsage = {
      plan_type: 'year',
      transcriptions_used: 20,
      transcriptions_limit: Infinity,
      transcriptions_remaining: Infinity,
      is_limited: false,
      renewal_date: '2024-06-16T00:00:00.000Z'
    };
    
    renderWithRouter(
      <SubscriptionNotification 
        usage={yearlyUsage} 
        subscription={null} 
      />
    );
    
    // Check badge text
    expect(screen.getByText('Premium')).toBeInTheDocument();
    
    // Check badge class
    const badge = screen.getByText('Premium').closest('.subscription-badge');
    expect(badge).toHaveClass('subscription-badge--premium');
  });

  test('renders limit reached state correctly', () => {
    const limitReachedUsage = {
      plan_type: 'free',
      transcriptions_used: 3,
      transcriptions_limit: 3,
      transcriptions_remaining: 0,
      is_limited: true,
      renewal_date: null
    };
    
    renderWithRouter(
      <SubscriptionNotification 
        usage={limitReachedUsage} 
        subscription={null} 
      />
    );
    
    // Check badge text
    expect(screen.getByText('Limit Reached')).toBeInTheDocument();
  });

  test('renders nothing when no usage provided', () => {
    const { container } = renderWithRouter(
      <SubscriptionNotification 
        usage={null} 
        subscription={null} 
      />
    );
    
    expect(container.firstChild).toBeNull();
  });

  test('links to subscription page', () => {
    const freeUsage = {
      plan_type: 'free',
      transcriptions_used: 1,
      transcriptions_limit: 3,
      transcriptions_remaining: 2,
      is_limited: true,
      renewal_date: null
    };
    
    renderWithRouter(
      <SubscriptionNotification 
        usage={freeUsage} 
        subscription={null} 
      />
    );
    
    // Check link destination
    const link = screen.getByText('2 Left').closest('a');
    expect(link).toHaveAttribute('href', '/subscription');
  });
}); 