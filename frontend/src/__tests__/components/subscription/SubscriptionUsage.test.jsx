import React from 'react';
import { render, screen } from '@testing-library/react';
import SubscriptionUsage from '../../../components/subscription/SubscriptionUsage';

describe('SubscriptionUsage component', () => {
  test('renders free plan usage correctly', () => {
    const freeUsage = {
      plan_type: 'free',
      transcriptions_used: 2,
      transcriptions_limit: 3,
      transcriptions_remaining: 1,
      is_limited: true,
      renewal_date: null
    };
    
    render(<SubscriptionUsage usage={freeUsage} />);
    
    // Check plan badge
    expect(screen.getByText('Free Plan')).toBeInTheDocument();
    
    // Check usage stats
    expect(screen.getByText('2')).toBeInTheDocument(); // Used
    expect(screen.getByText('3')).toBeInTheDocument(); // Limit
    expect(screen.getByText('1')).toBeInTheDocument(); // Remaining
    
    // Check progress bar text
    expect(screen.getByText('2 of 3 transcriptions used')).toBeInTheDocument();
  });

  test('renders premium monthly plan usage correctly', () => {
    const premiumUsage = {
      plan_type: 'month',
      transcriptions_used: 15,
      transcriptions_limit: Infinity,
      transcriptions_remaining: Infinity,
      is_limited: false,
      renewal_date: '2023-07-15T00:00:00.000Z'
    };
    
    render(<SubscriptionUsage usage={premiumUsage} />);
    
    // Check plan badge
    expect(screen.getByText('Monthly Premium')).toBeInTheDocument();
    
    // Check usage stats
    expect(screen.getByText('15')).toBeInTheDocument(); // Used
    expect(screen.getByText('Unlimited')).toBeInTheDocument(); // Limit
    expect(screen.getByText('∞')).toBeInTheDocument(); // Remaining
    
    // Check renewal date
    expect(screen.getByText('July 15, 2023')).toBeInTheDocument();
    
    // No progress bar for unlimited plan
    expect(screen.queryByText(/transcriptions used/)).not.toBeInTheDocument();
  });

  test('renders premium yearly plan usage correctly', () => {
    const yearlyUsage = {
      plan_type: 'year',
      transcriptions_used: 50,
      transcriptions_limit: Infinity,
      transcriptions_remaining: Infinity,
      is_limited: false,
      renewal_date: '2024-06-16T00:00:00.000Z'
    };
    
    render(<SubscriptionUsage usage={yearlyUsage} />);
    
    // Check plan badge
    expect(screen.getByText('Yearly Premium')).toBeInTheDocument();
    
    // Check usage stats
    expect(screen.getByText('50')).toBeInTheDocument(); // Used
    expect(screen.getByText('Unlimited')).toBeInTheDocument(); // Limit
    
    // Check renewal date
    expect(screen.getByText('June 16, 2024')).toBeInTheDocument();
  });

  test('renders progress bar correctly for limited plans', () => {
    const almostLimitUsage = {
      plan_type: 'free',
      transcriptions_used: 2,
      transcriptions_limit: 3,
      transcriptions_remaining: 1,
      is_limited: true,
      renewal_date: null
    };
    
    const { container } = render(<SubscriptionUsage usage={almostLimitUsage} />);
    
    // Check progress bar exists
    const progressFill = container.querySelector('.subscription-usage__progress-fill');
    expect(progressFill).toBeInTheDocument();
    
    // Check progress fill width (should be ~66%)
    expect(progressFill.style.width).toBe('66.66666666666667%');
  });

  test('renders nothing when no usage provided', () => {
    const { container } = render(<SubscriptionUsage usage={null} />);
    expect(container.firstChild).toBeNull();
  });

  test('handles limit reached state correctly', () => {
    const limitReachedUsage = {
      plan_type: 'free',
      transcriptions_used: 3,
      transcriptions_limit: 3,
      transcriptions_remaining: 0,
      is_limited: true,
      renewal_date: null
    };
    
    render(<SubscriptionUsage usage={limitReachedUsage} />);
    
    // Check stats show 0 remaining
    expect(screen.getByText('0')).toBeInTheDocument();
    
    // Progress bar should show 100%
    const progressText = screen.getByText('3 of 3 transcriptions used');
    expect(progressText).toBeInTheDocument();
  });
}); 