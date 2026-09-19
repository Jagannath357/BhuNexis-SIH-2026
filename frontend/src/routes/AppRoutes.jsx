import React from 'react';
import { Routes, Route } from 'react-router-dom';
import ProtectedRoute from './ProtectedRoute';

// Pages
import Home from '../pages/Home';
import Login from '../pages/Login';
import SignUp from '../pages/SignUp';
import AccessDenied from '../components/common/AccessDenied';
import NotFoundPage from '../pages/NotFoundPage';
import ProfilePage from '../pages/ProfilePage';
import MapViewPage from '../pages/MapViewPage';
import UploadDocumentPage from '../pages/UploadDocumentPage';

// Dashboards
import AdminDashboard from '../pages/dashboards/AdminDashboard';
import OfficerDashboard from '../pages/dashboards/OfficerDashboard';
import ReviewerDashboard from '../pages/dashboards/ReviewerDashboard';
import AuditorDashboard from '../pages/dashboards/AuditorDashboard';
import CitizenDashboard from '../pages/dashboards/CitizenDashboard';

// Feature Pages
import UserManagement from '../pages/admin/UserManagement';
import SystemSettings from '../pages/admin/SystemSettings';
import HumanReviewPage from '../pages/reviewer/HumanReviewPage';
import AuditLogsPage from '../pages/auditor/AuditLogsPage';
import CitizenSearch from '../pages/citizen/CitizenSearch';

export default function AppRoutes() {
  return (
    <Routes>
      {/* Public Pages */}
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/signup" element={<SignUp />} />

      {/* Admin Protected Routes: /a/* */}
      <Route
        path="/a/dashboard"
        element={
          <ProtectedRoute allowedRoles={['ADMIN']}>
            <AdminDashboard />
          </ProtectedRoute>
        }
      />
      <Route
        path="/a/users"
        element={
          <ProtectedRoute allowedRoles={['ADMIN']}>
            <UserManagement />
          </ProtectedRoute>
        }
      />
      <Route
        path="/a/settings"
        element={
          <ProtectedRoute allowedRoles={['ADMIN']}>
            <SystemSettings />
          </ProtectedRoute>
        }
      />

      {/* Officer Protected Routes: /o/* */}
      <Route
        path="/o/dashboard"
        element={
          <ProtectedRoute allowedRoles={['OFFICER']}>
            <OfficerDashboard />
          </ProtectedRoute>
        }
      />
      <Route
        path="/o/upload"
        element={
          <ProtectedRoute allowedRoles={['OFFICER', 'ADMIN']}>
            <UploadDocumentPage />
          </ProtectedRoute>
        }
      />

      {/* Reviewer Protected Routes: /r/* */}
      <Route
        path="/r/dashboard"
        element={
          <ProtectedRoute allowedRoles={['REVIEWER']}>
            <ReviewerDashboard />
          </ProtectedRoute>
        }
      />
      <Route
        path="/r/review"
        element={
          <ProtectedRoute allowedRoles={['REVIEWER', 'ADMIN']}>
            <HumanReviewPage />
          </ProtectedRoute>
        }
      />

      {/* Auditor Protected Routes: /au/* */}
      <Route
        path="/au/dashboard"
        element={
          <ProtectedRoute allowedRoles={['AUDITOR']}>
            <AuditorDashboard />
          </ProtectedRoute>
        }
      />
      <Route
        path="/au/audit"
        element={
          <ProtectedRoute allowedRoles={['AUDITOR', 'ADMIN']}>
            <AuditLogsPage />
          </ProtectedRoute>
        }
      />

      {/* Citizen Protected Routes: /u/* */}
      <Route
        path="/u/dashboard"
        element={
          <ProtectedRoute allowedRoles={['CITIZEN']}>
            <CitizenDashboard />
          </ProtectedRoute>
        }
      />
      <Route
        path="/u/search"
        element={
          <ProtectedRoute allowedRoles={['CITIZEN', 'ADMIN', 'OFFICER', 'REVIEWER', 'AUDITOR']}>
            <CitizenSearch />
          </ProtectedRoute>
        }
      />

      {/* Common Authenticated Routes */}
      <Route
        path="/map"
        element={
          <ProtectedRoute allowedRoles={['ADMIN', 'OFFICER', 'REVIEWER', 'AUDITOR', 'CITIZEN']}>
            <MapViewPage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/profile"
        element={
          <ProtectedRoute allowedRoles={['ADMIN', 'OFFICER', 'REVIEWER', 'AUDITOR', 'CITIZEN']}>
            <ProfilePage />
          </ProtectedRoute>
        }
      />

      {/* Access Denied & 404 */}
      <Route path="/access-denied" element={<AccessDenied />} />
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  );
}
