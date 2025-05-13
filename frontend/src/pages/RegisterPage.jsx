import React from 'react';
import Layout from '../components/layout/Layout';
import RegisterForm from '../components/auth/RegisterForm';

function RegisterPage() {
  return (
    <Layout>
      <div className="auth-page">
        <div className="container">
          <div className="auth-page__content">
            <RegisterForm />
          </div>
        </div>
      </div>
    </Layout>
  );
}

export default RegisterPage; 