# React Frontend Guidelines

This document outlines the key principles, patterns, and best practices for working with React in this project. It serves as a reference for AI agents to understand our React architecture and implementation approach.

## Core React Concepts

### Components

React applications are built from components - reusable pieces of UI that render based on props and state. We use two types:

- **Functional Components** (preferred): JavaScript functions that accept props and return React elements
- **Class Components**: Classes that extend `React.Component` and implement a render method

```jsx
// Functional component (preferred)
function Welcome(props) {
  return <h1>Hello, {props.name}</h1>;
}

// Class component (legacy)
class Welcome extends React.Component {
  render() {
    return <h1>Hello, {this.props.name}</h1>;
  }
}
```

### JSX

We use JSX syntax for defining UI elements. JSX is transformed into React.createElement() calls during build:

```jsx
// JSX syntax
const element = <h1 className="greeting">Hello, world!</h1>;

// Equivalent JavaScript
const element = React.createElement(
  'h1',
  {className: 'greeting'},
  'Hello, world!'
);
```

### Props and State

- **Props**: Read-only data passed from parent to child components
- **State**: Mutable data managed within a component using useState or class state

```jsx
// Props example
function Welcome(props) {
  return <h1>Hello, {props.name}</h1>;
}

// State example with useState hook
function Counter() {
  const [count, setCount] = useState(0);
  return (
    <div>
      <p>You clicked {count} times</p>
      <button onClick={() => setCount(count + 1)}>
        Click me
      </button>
    </div>
  );
}
```

### Hooks

We use React hooks for stateful logic in functional components:

- **useState**: Adds state to functional components
- **useEffect**: Handles side effects like data fetching or subscriptions
- **useContext**: Accesses context values without prop drilling
- **useRef**: Creates mutable references that persist across renders
- **useMemo/useCallback**: Optimize performance by memoizing values/functions

```jsx
import { useState, useEffect, useContext, useRef, useMemo, useCallback } from 'react';

function ExampleComponent() {
  // useState
  const [data, setData] = useState(null);
  
  // useEffect
  useEffect(() => {
    fetchData().then(result => setData(result));
    return () => {
      // cleanup code
    };
  }, []);
  
  // useRef
  const inputRef = useRef(null);
  
  // useMemo
  const processedData = useMemo(() => {
    return data ? processData(data) : null;
  }, [data]);
  
  // useCallback
  const handleClick = useCallback(() => {
    console.log(data);
  }, [data]);
  
  return (
    <div>
      <input ref={inputRef} />
      <button onClick={handleClick}>Click me</button>
    </div>
  );
}
```

## Project Structure

We follow a feature-based organization pattern:

```
src/
├── assets/           # Static assets like images, fonts
├── components/       # Shared/reusable components
│   ├── Button/
│   ├── Input/
│   └── Layout/
├── features/         # Feature-specific code
│   ├── Auth/
│   ├── Dashboard/
│   └── Settings/
├── hooks/            # Custom React hooks
├── context/          # React context providers
├── utils/            # Helper functions
├── services/         # API services
├── styles/           # Global styles
├── App.jsx           # Root component
└── index.jsx         # Entry point
```

## State Management

Based on complexity, we use:

1. **Component State**: For local component state using useState
2. **Context API**: For sharing state across component trees without prop drilling
3. **Redux**: For complex applications with many state interactions
4. **React Query**: For server state management

### Context API Example

```jsx
// Create context
const ThemeContext = React.createContext('light');

// Provider component
function App() {
  const [theme, setTheme] = useState('light');
  
  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      <ThemedButton />
    </ThemeContext.Provider>
  );
}

// Consumer component
function ThemedButton() {
  const { theme, setTheme } = useContext(ThemeContext);
  
  return (
    <button
      onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}
      style={{ background: theme === 'light' ? '#fff' : '#333', color: theme === 'light' ? '#333' : '#fff' }}
    >
      Toggle Theme
    </button>
  );
}
```

## Styling Approaches

We support multiple styling methods:

1. **CSS Modules**: Scoped CSS files with className imports
2. **Styled Components**: CSS-in-JS library for dynamic styling
3. **Tailwind CSS**: Utility-first CSS framework
4. **CSS-in-JS**: Inline styles for dynamic styling

```jsx
// CSS Modules
import styles from './Button.module.css';
function Button() {
  return <button className={styles.button}>Click Me</button>;
}

// Styled Components
import styled from 'styled-components';
const StyledButton = styled.button`
  background: ${props => props.primary ? 'blue' : 'white'};
  color: ${props => props.primary ? 'white' : 'blue'};
`;
function Button() {
  return <StyledButton primary>Click Me</StyledButton>;
}

// Tailwind
function Button() {
  return <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
    Click Me
  </button>;
}
```

## Routing

We use React Router for navigation:

```jsx
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';

function App() {
  return (
    <BrowserRouter>
      <nav>
        <Link to="/">Home</Link>
        <Link to="/about">About</Link>
      </nav>
      
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/users/:userId" element={<UserProfile />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
}
```

## Forms Management

For forms, we primarily use:

1. **Controlled Components**: Form elements controlled by React state
2. **React Hook Form**: For complex form management
3. **Formik**: Alternative form library for validation and handling

```jsx
// Controlled component example
function SimpleForm() {
  const [value, setValue] = useState('');
  
  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Submitted:', value);
  };
  
  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={value}
        onChange={(e) => setValue(e.target.value)}
      />
      <button type="submit">Submit</button>
    </form>
  );
}

// React Hook Form example
import { useForm } from 'react-hook-form';

function ComplexForm() {
  const { register, handleSubmit, formState: { errors } } = useForm();
  
  const onSubmit = (data) => console.log(data);
  
  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('firstName', { required: true })} />
      {errors.firstName && <span>This field is required</span>}
      
      <input {...register('email', { 
        required: true,
        pattern: /^\S+@\S+$/i 
      })} />
      {errors.email && <span>Valid email is required</span>}
      
      <button type="submit">Submit</button>
    </form>
  );
}
```

## Data Fetching

For API interactions, we recommend:

1. **useEffect + fetch**: Simple approach for basic needs
2. **React Query**: Preferred for complex data fetching with caching
3. **SWR**: Alternative to React Query with similar benefits
4. **Axios**: HTTP client for more complex request configurations

```jsx
// Basic fetch with useEffect
function UserList() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const response = await fetch('https://api.example.com/users');
        if (!response.ok) throw new Error('Network response was not ok');
        const data = await response.json();
        setUsers(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    
    fetchUsers();
  }, []);
  
  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;
  
  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}

// React Query example
import { useQuery } from 'react-query';

function UserList() {
  const fetchUsers = async () => {
    const res = await fetch('https://api.example.com/users');
    if (!res.ok) throw new Error('Network response was not ok');
    return res.json();
  };
  
  const { data: users, isLoading, error } = useQuery('users', fetchUsers);
  
  if (isLoading) return <p>Loading...</p>;
  if (error) return <p>Error: {error.message}</p>;
  
  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
```

## Testing

We use the following testing tools:

1. **Jest**: Test runner and assertion library
2. **React Testing Library**: Component testing with user-centric approach
3. **Cypress**: End-to-end testing

```jsx
// React Testing Library example
import { render, screen, fireEvent } from '@testing-library/react';
import Counter from './Counter';

test('counter increments when button is clicked', () => {
  render(<Counter />);
  
  // Initial state check
  expect(screen.getByText(/you clicked 0 times/i)).toBeInTheDocument();
  
  // Interact with the component
  fireEvent.click(screen.getByRole('button', { name: /click me/i }));
  
  // Check updated state
  expect(screen.getByText(/you clicked 1 times/i)).toBeInTheDocument();
});
```

## Performance Optimization

Key techniques for optimizing React applications:

1. **React.memo**: Prevent unnecessary re-renders of functional components
2. **useMemo/useCallback**: Memoize expensive calculations and functions
3. **Code Splitting**: Split code into smaller chunks loaded on demand
4. **Virtualization**: Render only visible items in large lists
5. **Lazy Loading**: Load components only when needed

```jsx
// React.memo example
const MemoizedComponent = React.memo(function MyComponent(props) {
  // Only re-renders if props change
  return <div>{props.name}</div>;
});

// Code splitting with lazy and Suspense
import React, { Suspense, lazy } from 'react';

const LazyComponent = lazy(() => import('./LazyComponent'));

function MyComponent() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <LazyComponent />
    </Suspense>
  );
}

// Virtualization with react-window
import { FixedSizeList } from 'react-window';

function VirtualizedList({ items }) {
  const Row = ({ index, style }) => (
    <div style={style}>Item {items[index]}</div>
  );
  
  return (
    <FixedSizeList
      height={500}
      width={300}
      itemCount={items.length}
      itemSize={35}
    >
      {Row}
    </FixedSizeList>
  );
}
```

## Accessibility (a11y)

All components should follow these accessibility practices:

1. Use semantic HTML elements
2. Include proper ARIA attributes when necessary
3. Ensure keyboard navigation works
4. Maintain sufficient color contrast
5. Support screen readers

```jsx
// Accessible button example
function AccessibleButton({ onClick, disabled, children }) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      aria-disabled={disabled}
      aria-label="Custom action button"
      tabIndex={0}
    >
      {children}
    </button>
  );
}
```

## Error Handling

Handle errors with React Error Boundaries:

```jsx
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    console.error("Error caught:", error, errorInfo);
    // Report to error tracking service
  }

  render() {
    if (this.state.hasError) {
      return <h1>Something went wrong.</h1>;
    }

    return this.props.children;
  }
}

// Usage
<ErrorBoundary>
  <MyComponent />
</ErrorBoundary>
```

## Environment Variables

Access environment variables using the `process.env.REACT_APP_*` prefix:

```jsx
// Accessing environment variables
const apiUrl = process.env.REACT_APP_API_URL;

function ApiComponent() {
  const [data, setData] = useState(null);
  
  useEffect(() => {
    fetch(`${apiUrl}/endpoint`)
      .then(res => res.json())
      .then(setData);
  }, []);
  
  return <div>{/* render data */}</div>;
}
```

## Build and Deployment

Our build process uses:

- Development server: `npm start` or `yarn start`
- Production build: `npm run build` or `yarn build`
- Environment-specific builds using `.env` files

## Project-Specific Patterns

### Component Creation Conventions

1. **One component per file**: Each component should be in its own file
2. **Named exports for components**: `export function ComponentName()`
3. **Index files for folders**: Use barrel exports in index.js files

### Prop Validation

Use PropTypes or TypeScript for prop validation:

```jsx
// With PropTypes
import PropTypes from 'prop-types';

function User({ name, age, isActive }) {
  return (
    <div>
      <h2>{name}</h2>
      <p>Age: {age}</p>
      <p>Status: {isActive ? 'Active' : 'Inactive'}</p>
    </div>
  );
}

User.propTypes = {
  name: PropTypes.string.isRequired,
  age: PropTypes.number,
  isActive: PropTypes.bool
};

User.defaultProps = {
  age: 0,
  isActive: false
};

// With TypeScript
interface UserProps {
  name: string;
  age?: number;
  isActive?: boolean;
}

function User({ name, age = 0, isActive = false }: UserProps) {
  return (
    <div>
      <h2>{name}</h2>
      <p>Age: {age}</p>
      <p>Status: {isActive ? 'Active' : 'Inactive'}</p>
    </div>
  );
}
```

### Custom Hooks

Create reusable logic with custom hooks:

```jsx
// Custom hook for form input
function useInput(initialValue = '') {
  const [value, setValue] = useState(initialValue);
  
  const handleChange = (e) => {
    setValue(e.target.value);
  };
  
  const reset = () => {
    setValue(initialValue);
  };
  
  return {
    value,
    onChange: handleChange,
    reset,
    bind: {
      value,
      onChange: handleChange
    }
  };
}

// Usage
function Form() {
  const { value: firstName, bind: bindFirstName, reset: resetFirstName } = useInput('');
  const { value: lastName, bind: bindLastName, reset: resetLastName } = useInput('');
  
  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Submitted:', firstName, lastName);
    resetFirstName();
    resetLastName();
  };
  
  return (
    <form onSubmit={handleSubmit}>
      <input type="text" placeholder="First Name" {...bindFirstName} />
      <input type="text" placeholder="Last Name" {...bindLastName} />
      <button type="submit">Submit</button>
    </form>
  );
}
```

## Common Pitfalls to Avoid

1. **Infinite re-render loops**: Missing dependency arrays in useEffect or updating state in render
2. **Memory leaks**: Not cleaning up subscriptions or timers in useEffect
3. **Prop drilling**: Passing props through many levels (use Context instead)
4. **Direct DOM manipulation**: Avoid except when absolutely necessary
5. **Premature optimization**: Optimize only after identifying performance issues

## Learning Resources

- [React Official Documentation](https://react.dev/)
- [React Patterns](https://reactpatterns.com/)
- [React Hooks API Reference](https://react.dev/reference/react)
- [React Router Documentation](https://reactrouter.com/)

## Conclusion

This document covers the essentials of React development for our project. When writing or reviewing React code, refer to these guidelines to ensure consistency and best practices across the codebase.
