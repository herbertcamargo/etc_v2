import React, { forwardRef } from 'react';
import PropTypes from 'prop-types';

/**
 * Input component - A flexible, reusable input component
 */
const Input = forwardRef(({
  type = 'text',
  id,
  name,
  value,
  onChange,
  onBlur,
  placeholder,
  label,
  error,
  disabled = false,
  required = false,
  className = '',
  ...props
}, ref) => {
  return (
    <div className="form-group">
      {label && (
        <label htmlFor={id || name}>
          {label}
          {required && <span className="required">*</span>}
        </label>
      )}
      
      <input
        ref={ref}
        type={type}
        id={id || name}
        name={name}
        value={value}
        onChange={onChange}
        onBlur={onBlur}
        placeholder={placeholder}
        className={`input ${error ? 'input--error' : ''} ${className}`}
        disabled={disabled}
        required={required}
        {...props}
      />
      
      {error && <div className="input-error">{error}</div>}
    </div>
  );
});

Input.propTypes = {
  type: PropTypes.string,
  id: PropTypes.string,
  name: PropTypes.string.isRequired,
  value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
  onChange: PropTypes.func,
  onBlur: PropTypes.func,
  placeholder: PropTypes.string,
  label: PropTypes.string,
  error: PropTypes.string,
  disabled: PropTypes.bool,
  required: PropTypes.bool,
  className: PropTypes.string,
};

Input.displayName = 'Input';

export default Input; 