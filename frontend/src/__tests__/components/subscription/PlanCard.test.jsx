import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import PlanCard from '../../../components/subscription/PlanCard';

describe('PlanCard component', () => {
  const mockPlan = {
    id: 'price_monthly',
    name: 'Monthly Plan',
    description: 'Unlimited transcriptions with full features',
    price: 4.99,
    currency: 'USD',
    interval: 'month',
    features: [
      'Unlimited transcriptions',
      'Advanced analytics',
      'Priority support'
    ]
  };

  const mockSelectHandler = jest.fn();

  beforeEach(() => {
    mockSelectHandler.mockClear();
  });

  test('renders plan information correctly', () => {
    render(<PlanCard plan={mockPlan} onSelect={mockSelectHandler} />);
    
    // Check plan name and description
    expect(screen.getByText('Monthly Plan')).toBeInTheDocument();
    expect(screen.getByText('Unlimited transcriptions with full features')).toBeInTheDocument();
    
    // Check price and interval
    expect(screen.getByText('$4.99')).toBeInTheDocument();
    expect(screen.getByText('/monthly')).toBeInTheDocument();
    
    // Check features
    mockPlan.features.forEach(feature => {
      expect(screen.getByText(feature)).toBeInTheDocument();
    });
    
    // Check button text
    expect(screen.getByRole('button')).toHaveTextContent('Select Plan');
  });

  test('selects plan when clicked', () => {
    render(<PlanCard plan={mockPlan} onSelect={mockSelectHandler} />);
    
    // Click the select button
    fireEvent.click(screen.getByRole('button'));
    
    // Check that selection handler was called with plan ID
    expect(mockSelectHandler).toHaveBeenCalledWith('price_monthly');
  });

  test('shows selected state when selected', () => {
    render(<PlanCard plan={mockPlan} onSelect={mockSelectHandler} isSelected={true} />);
    
    // Check button text changes to "Selected"
    expect(screen.getByRole('button')).toHaveTextContent('Selected');
    
    // Check class for selected state
    const cardElement = screen.getByText('Monthly Plan').closest('.plan-card');
    expect(cardElement).toHaveClass('plan-card--selected');
  });

  test('shows loading state when processing', () => {
    render(<PlanCard plan={mockPlan} onSelect={mockSelectHandler} isLoading={true} />);
    
    // Check button text changes to loading
    expect(screen.getByRole('button')).toHaveTextContent('Processing...');
    
    // Check button is disabled
    expect(screen.getByRole('button')).toBeDisabled();
  });

  test('renders nothing when no plan provided', () => {
    const { container } = render(<PlanCard plan={null} onSelect={mockSelectHandler} />);
    expect(container.firstChild).toBeNull();
  });

  test('formats currency correctly', () => {
    const expensivePlan = {
      ...mockPlan,
      price: 1234.56
    };
    
    render(<PlanCard plan={expensivePlan} onSelect={mockSelectHandler} />);
    expect(screen.getByText('$1,234.56')).toBeInTheDocument();
  });

  test('handles yearly plan interval correctly', () => {
    const yearlyPlan = {
      ...mockPlan,
      interval: 'year'
    };
    
    render(<PlanCard plan={yearlyPlan} onSelect={mockSelectHandler} />);
    expect(screen.getByText('/yearly')).toBeInTheDocument();
  });
}); 