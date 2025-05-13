import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import Button from '../common/Button';
import Input from '../common/Input';

function LoginForm() {
  const [formData, setFormData] = useState({
    username: '',
    password: '',
  });
  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  
  // Get the page to redirect to after login (or default to dashboard)
  const from = location.state?.from?.pathname || '/dashboard';
  
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
    
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors((prev) => ({
        ...prev,
        [name]: '',
      }));
    }
  };
  
  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.username.trim()) {
      newErrors.username = 'Username is required';
    }
    
    if (!formData.password) {
      newErrors.password = 'Password is required';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }
    
    setIsSubmitting(true);
    
    try {
      await login(formData);
      navigate(from, { replace: true });
    } catch (error) {
      setErrors({
        general: error.message || 'Failed to login. Please try again.',
      });
      setIsSubmitting(false);
    }
  };
  
  return (
    <div className="auth-form-container">
      <h2 className="auth-form-title">Login to Your Account</h2>
      
      {errors.general && (
        <div className="auth-form-error">{errors.general}</div>
      )}
      
      <form className="auth-form" onSubmit={handleSubmit}>
        <Input
          type="text"
          name="username"
          label="Username"
          value={formData.username}
          onChange={handleChange}
          error={errors.username}
          required
        />
        
        <Input
          type="password"
          name="password"
          label="Password"
          value={formData.password}
          onChange={handleChange}
          error={errors.password}
          required
        />
        
        <div className="auth-form-options">
          <label className="checkbox-label">
            <input type="checkbox" name="remember" />
            <span>Remember me</span>
          </label>
          
          <Link to="/forgot-password" className="auth-form-link">
            Forgot password?
          </Link>
        </div>
        
        <Button
          type="submit"
          variant="primary"
          fullWidth
          disabled={isSubmitting}
        >
          {isSubmitting ? 'Logging in...' : 'Login'}
        </Button>
        
        <div className="auth-form-footer">
          <p>
            Don't have an account?{' '}
            <Link to="/register" className="auth-form-link">
              Register
            </Link>
          </p>
        </div>
      </form>
    </div>
  );
}

export default LoginForm; 