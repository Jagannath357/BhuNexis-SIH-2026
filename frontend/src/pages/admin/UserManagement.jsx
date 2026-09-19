import React, { useEffect, useState } from 'react';
import DashboardLayout from '../../components/layout/DashboardLayout';
import userService from '../../services/userService';
import StatusBadge from '../../components/common/StatusBadge';
import { Users, UserPlus, Shield, CheckCircle, XCircle, Search, Mail, Lock, Phone } from 'lucide-react';

export default function UserManagement() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);
  const [msg, setMsg] = useState(null);

  // New User Form State
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('password123');
  const [role, setRole] = useState('OFFICER');
  const [phone, setPhone] = useState('');

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    setLoading(true);
    try {
      const data = await userService.getUsers();
      setUsers(data);
    } catch (err) {
      console.error("Failed to fetch users:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleToggleStatus = async (user) => {
    try {
      await userService.updateUserStatus(user.id, !user.is_active);
      setMsg(`User ${user.email} status updated to ${!user.is_active ? 'ACTIVE' : 'DEACTIVATED'}.`);
      fetchUsers();
      setTimeout(() => setMsg(null), 3000);
    } catch (err) {
      alert("Failed to update status: " + (err.message || 'Error'));
    }
  };

  const handleCreateUser = async (e) => {
    e.preventDefault();
    try {
      await userService.createUser({
        full_name: fullName,
        email,
        password,
        role,
        phone,
        is_active: true
      });
      setMsg(`Internal user ${email} created successfully!`);
      setModalOpen(false);
      setFullName('');
      setEmail('');
      fetchUsers();
      setTimeout(() => setMsg(null), 4000);
    } catch (err) {
      alert("Create user failed: " + (err.message || 'Error'));
    }
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl md:text-3xl font-extrabold text-[var(--text-primary)] tracking-tight">
              Internal User & Credential Provisioning
            </h1>
            <p className="text-sm text-[var(--text-secondary)] mt-1">
              Manage system administrator, officer, reviewer, auditor, and citizen accounts
            </p>
          </div>
          <button
            onClick={() => setModalOpen(true)}
            className="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-xl text-sm transition-all shadow-lg shadow-indigo-600/30 flex items-center space-x-2 cursor-pointer"
          >
            <UserPlus className="w-4 h-4" />
            <span>Create Internal User</span>
          </button>
        </div>

        {msg && (
          <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-600 dark:text-emerald-400 text-xs font-bold flex items-center space-x-2">
            <CheckCircle className="w-5 h-5 text-emerald-500" />
            <span>{msg}</span>
          </div>
        )}

        {/* User Table */}
        <div className="bg-[var(--bg-card)] border border-[var(--border-color)] rounded-2xl p-6 shadow-sm">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead>
                <tr className="border-b border-[var(--border-color)] text-[var(--text-secondary)] uppercase text-xs">
                  <th className="py-3 px-4">ID</th>
                  <th className="py-3 px-4">Full Name</th>
                  <th className="py-3 px-4">Email</th>
                  <th className="py-3 px-4">Role</th>
                  <th className="py-3 px-4">Phone</th>
                  <th className="py-3 px-4">Status</th>
                  <th className="py-3 px-4">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[var(--border-color)]">
                {users.map((u) => (
                  <tr key={u.id} className="hover:bg-[var(--bg-main)]">
                    <td className="py-3.5 px-4 font-mono font-bold text-indigo-500">#{u.id}</td>
                    <td className="py-3.5 px-4 font-bold text-[var(--text-primary)]">{u.full_name}</td>
                    <td className="py-3.5 px-4 text-[var(--text-secondary)]">{u.email}</td>
                    <td className="py-3.5 px-4">
                      <span className="px-2.5 py-1 text-xs font-bold rounded bg-indigo-500/10 text-indigo-600 dark:text-indigo-400 border border-indigo-500/30">
                        {u.role}
                      </span>
                    </td>
                    <td className="py-3.5 px-4 text-xs text-[var(--text-muted)]">{u.phone || 'N/A'}</td>
                    <td className="py-3.5 px-4">
                      <StatusBadge status={u.is_active ? 'HEALTHY' : 'DEACTIVATED'} />
                    </td>
                    <td className="py-3.5 px-4">
                      <button
                        onClick={() => handleToggleStatus(u)}
                        className={`px-3 py-1.5 text-xs font-bold rounded-lg transition-all cursor-pointer ${
                          u.is_active
                            ? 'bg-rose-500/10 text-rose-600 dark:text-rose-400 hover:bg-rose-500/20'
                            : 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 hover:bg-emerald-500/20'
                        }`}
                      >
                        {u.is_active ? 'Deactivate' : 'Activate'}
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Create User Modal */}
        {modalOpen && (
          <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
            <div className="max-w-md w-full bg-[var(--bg-card)] border border-[var(--border-color)] rounded-2xl p-6 shadow-2xl space-y-4">
              <div className="flex items-center justify-between pb-3 border-b border-[var(--border-color)]">
                <h3 className="font-bold text-lg text-[var(--text-primary)]">Provision Internal Credentials</h3>
                <button onClick={() => setModalOpen(false)} className="text-xs text-[var(--text-muted)] hover:text-[var(--text-primary)] cursor-pointer">Close</button>
              </div>

              <form onSubmit={handleCreateUser} className="space-y-4">
                <div>
                  <label className="block text-xs font-semibold uppercase text-[var(--text-secondary)] mb-1">Full Name</label>
                  <input type="text" required value={fullName} onChange={(e) => setFullName(e.target.value)} className="w-full px-3.5 py-2 rounded-xl border border-[var(--border-color)] bg-[var(--bg-main)] text-[var(--text-primary)] text-xs" />
                </div>
                <div>
                  <label className="block text-xs font-semibold uppercase text-[var(--text-secondary)] mb-1">Email Address</label>
                  <input type="email" required value={email} onChange={(e) => setEmail(e.target.value)} className="w-full px-3.5 py-2 rounded-xl border border-[var(--border-color)] bg-[var(--bg-main)] text-[var(--text-primary)] text-xs" />
                </div>
                <div>
                  <label className="block text-xs font-semibold uppercase text-[var(--text-secondary)] mb-1">Assigned Role</label>
                  <select value={role} onChange={(e) => setRole(e.target.value)} className="w-full px-3.5 py-2 rounded-xl border border-[var(--border-color)] bg-[var(--bg-main)] text-[var(--text-primary)] text-xs font-bold">
                    <option value="ADMIN">ADMIN</option>
                    <option value="OFFICER">OFFICER</option>
                    <option value="REVIEWER">REVIEWER</option>
                    <option value="AUDITOR">AUDITOR</option>
                    <option value="CITIZEN">CITIZEN</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-semibold uppercase text-[var(--text-secondary)] mb-1">Initial Password</label>
                  <input type="text" required value={password} onChange={(e) => setPassword(e.target.value)} className="w-full px-3.5 py-2 rounded-xl border border-[var(--border-color)] bg-[var(--bg-main)] text-[var(--text-primary)] text-xs font-mono" />
                </div>
                <div>
                  <label className="block text-xs font-semibold uppercase text-[var(--text-secondary)] mb-1">Mobile Phone (Optional)</label>
                  <input type="tel" value={phone} onChange={(e) => setPhone(e.target.value)} className="w-full px-3.5 py-2 rounded-xl border border-[var(--border-color)] bg-[var(--bg-main)] text-[var(--text-primary)] text-xs" />
                </div>

                <div className="pt-3 flex space-x-3">
                  <button type="button" onClick={() => setModalOpen(false)} className="w-1/2 py-2.5 rounded-xl border border-[var(--border-color)] text-[var(--text-secondary)] text-xs font-semibold">Cancel</button>
                  <button type="submit" className="w-1/2 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold rounded-xl">Save User</button>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}
