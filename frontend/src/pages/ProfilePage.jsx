import React, { useState } from 'react';
import DashboardLayout from '../components/layout/DashboardLayout';
import { useAuth } from '../context/AuthContext';
import userService from '../services/userService';
import { User, Lock, CheckCircle, AlertCircle, Save } from 'lucide-react';

export default function ProfilePage() {
  const { user, updateUser } = useAuth();

  const [fullName, setFullName] = useState(user?.full_name || '');
  const [phone, setPhone] = useState(user?.phone || '');

  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');

  const [profileMsg, setProfileMsg] = useState(null);
  const [passwordMsg, setPasswordMsg] = useState(null);
  const [error, setError] = useState(null);

  const handleProfileSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    try {
      const updated = await userService.updateProfile({ full_name: fullName, phone });
      updateUser(updated);
      setProfileMsg("Profile details updated successfully!");
      setTimeout(() => setProfileMsg(null), 4000);
    } catch (err) {
      setError(err?.message || "Failed to update profile.");
    }
  };

  const handlePasswordSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    try {
      await userService.updatePassword(currentPassword, newPassword);
      setPasswordMsg("Password changed successfully!");
      setCurrentPassword('');
      setNewPassword('');
      setTimeout(() => setPasswordMsg(null), 4000);
    } catch (err) {
      setError(err?.message || "Password change failed.");
    }
  };

  return (
    <DashboardLayout>
      <div className="max-w-3xl mx-auto space-y-6">
        <div>
          <h1 className="text-2xl md:text-3xl font-extrabold text-[var(--text-primary)] tracking-tight">
            Account Profile & Credentials
          </h1>
          <p className="text-sm text-[var(--text-secondary)] mt-1">
            Manage your personal profile information & account security password
          </p>
        </div>

        {error && (
          <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-600 dark:text-rose-400 text-xs font-semibold flex items-center space-x-2">
            <AlertCircle className="w-5 h-5 flex-shrink-0 text-rose-500" />
            <span>{error}</span>
          </div>
        )}

        {profileMsg && (
          <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-600 dark:text-emerald-400 text-xs font-semibold flex items-center space-x-2">
            <CheckCircle className="w-5 h-5 text-emerald-500" />
            <span>{profileMsg}</span>
          </div>
        )}

        {passwordMsg && (
          <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-600 dark:text-emerald-400 text-xs font-semibold flex items-center space-x-2">
            <CheckCircle className="w-5 h-5 text-emerald-500" />
            <span>{passwordMsg}</span>
          </div>
        )}

        {/* Profile Details Form */}
        <form onSubmit={handleProfileSubmit} className="bg-[var(--bg-card)] border border-[var(--border-color)] rounded-2xl p-6 shadow-sm space-y-4">
          <h3 className="text-lg font-bold text-[var(--text-primary)] pb-2 border-b border-[var(--border-color)]">Personal Details</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold uppercase text-[var(--text-secondary)] mb-1">Full Name</label>
              <input
                type="text"
                required
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                className="w-full px-3.5 py-2.5 rounded-xl border border-[var(--border-color)] bg-[var(--bg-main)] text-[var(--text-primary)] text-sm font-semibold"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold uppercase text-[var(--text-secondary)] mb-1">Email Address</label>
              <input
                type="email"
                disabled
                value={user?.email || ''}
                className="w-full px-3.5 py-2.5 rounded-xl border border-[var(--border-color)] bg-[var(--bg-main)] text-[var(--text-muted)] text-sm font-semibold cursor-not-allowed"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold uppercase text-[var(--text-secondary)] mb-1">System Role</label>
              <input
                type="text"
                disabled
                value={user?.role || ''}
                className="w-full px-3.5 py-2.5 rounded-xl border border-[var(--border-color)] bg-[var(--bg-main)] text-emerald-500 font-bold text-sm uppercase cursor-not-allowed"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold uppercase text-[var(--text-secondary)] mb-1">Mobile Phone</label>
              <input
                type="tel"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                placeholder="9876543210"
                className="w-full px-3.5 py-2.5 rounded-xl border border-[var(--border-color)] bg-[var(--bg-main)] text-[var(--text-primary)] text-sm"
              />
            </div>
          </div>

          <button
            type="submit"
            className="py-2.5 px-5 bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs rounded-xl transition-all shadow-md shadow-emerald-600/20 flex items-center space-x-2 cursor-pointer"
          >
            <Save className="w-4 h-4" />
            <span>Update Profile Info</span>
          </button>
        </form>

        {/* Password Change Form */}
        <form onSubmit={handlePasswordSubmit} className="bg-[var(--bg-card)] border border-[var(--border-color)] rounded-2xl p-6 shadow-sm space-y-4">
          <h3 className="text-lg font-bold text-[var(--text-primary)] pb-2 border-b border-[var(--border-color)]">Change Password</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold uppercase text-[var(--text-secondary)] mb-1">Current Password</label>
              <input
                type="password"
                required
                value={currentPassword}
                onChange={(e) => setCurrentPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full px-3.5 py-2.5 rounded-xl border border-[var(--border-color)] bg-[var(--bg-main)] text-[var(--text-primary)] text-sm"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold uppercase text-[var(--text-secondary)] mb-1">New Password</label>
              <input
                type="password"
                required
                minLength={6}
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full px-3.5 py-2.5 rounded-xl border border-[var(--border-color)] bg-[var(--bg-main)] text-[var(--text-primary)] text-sm"
              />
            </div>
          </div>

          <button
            type="submit"
            className="py-2.5 px-5 bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs rounded-xl transition-all shadow-md shadow-emerald-600/20 flex items-center space-x-2 cursor-pointer"
          >
            <Lock className="w-4 h-4" />
            <span>Change Password</span>
          </button>
        </form>
      </div>
    </DashboardLayout>
  );
}
