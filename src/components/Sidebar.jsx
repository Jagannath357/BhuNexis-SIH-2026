import React from 'react';
import { NavLink } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { 
  LayoutDashboard, 
  UploadCloud, 
  MapPin, 
  FileCheck, 
  Users, 
  Sliders, 
  History, 
  User, 
  Search, 
  ShieldCheck,
  Building,
  Sparkles
} from 'lucide-react';

export function Sidebar({ isOpen, onClose }) {
  const { user } = useAuth();
  if (!user) return null;

  const role = user.role;

  const getNavLinks = () => {
    switch (role) {
      case 'ADMIN':
        return [
          { to: '/a/dashboard', label: 'System Overview', icon: LayoutDashboard },
          { to: '/a/upload', label: 'Ingestion Pipeline', icon: UploadCloud },
          { to: '/a/map', label: 'Cadastral GIS Map', icon: MapPin },
          { to: '/a/users', label: 'User Management', icon: Users },
          { to: '/a/settings', label: 'System Settings', icon: Sliders },
          { to: '/a/audit', label: 'Compliance Audit', icon: History },
          { to: '/a/profile', label: 'Admin Profile', icon: User }
        ];

      case 'OFFICER':
        return [
          { to: '/o/dashboard', label: 'Ingestion Dashboard', icon: LayoutDashboard },
          { to: '/o/upload', label: 'Upload & Process', icon: UploadCloud },
          { to: '/o/map', label: 'Cadastral GIS View', icon: MapPin },
          { to: '/o/profile', label: 'Officer Profile', icon: User }
        ];

      case 'REVIEWER':
        return [
          { to: '/r/dashboard', label: 'Verification Center', icon: LayoutDashboard },
          { to: '/r/review', label: 'Human Review Queue', icon: FileCheck, badge: 'Active' },
          { to: '/r/map', label: 'GIS Boundary Match', icon: MapPin },
          { to: '/r/profile', label: 'Reviewer Profile', icon: User }
        ];

      case 'AUDITOR':
        return [
          { to: '/au/dashboard', label: 'Compliance Overview', icon: LayoutDashboard },
          { to: '/au/audit', label: 'Audit Trail Logs', icon: History },
          { to: '/au/map', label: 'Inspection GIS Map', icon: MapPin },
          { to: '/au/profile', label: 'Auditor Profile', icon: User }
        ];

      case 'CITIZEN':
      default:
        return [
          { to: '/u/dashboard', label: 'Land Records Portal', icon: LayoutDashboard },
          { to: '/u/search', label: 'Search Land Records', icon: Search },
          { to: '/u/map', label: 'Public Land Explorer', icon: MapPin },
          { to: '/u/profile', label: 'Citizen Profile', icon: User }
        ];
    }
  };

  const navLinks = getNavLinks();

  return (
    <>
      {/* Mobile Backdrop */}
      {isOpen && (
        <div 
          onClick={onClose}
          className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-40 lg:hidden"
        />
      )}

      {/* Sidebar Panel */}
      <aside className={`
        fixed lg:static top-[57px] bottom-0 left-0 z-40
        w-64 bg-white dark:bg-slate-900 text-slate-700 dark:text-slate-300 border-r border-slate-200 dark:border-slate-800
        flex flex-col justify-between transition-all duration-200 ease-in-out
        ${isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
      `}>
        {/* Upper Menu List */}
        <div className="p-4 space-y-6 overflow-y-auto flex-1">
          {/* User Status Card */}
          <div className="bg-slate-50 dark:bg-slate-800/80 rounded-xl p-3.5 border border-slate-200 dark:border-slate-700/60 shadow-sm">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-sky-500/10 border border-sky-500/30 flex items-center justify-center text-sky-600 dark:text-sky-400 font-bold shrink-0">
                <ShieldCheck className="w-5 h-5" />
              </div>
              <div className="overflow-hidden">
                <div className="text-xs font-bold text-slate-900 dark:text-white truncate">{user.roleDisplayName}</div>
                <div className="text-[10px] text-sky-600 dark:text-sky-400 font-semibold uppercase tracking-wider">{user.role} ACCESS</div>
              </div>
            </div>
          </div>

          {/* Navigation Links */}
          <nav className="space-y-1">
            <p className="px-3 text-[10px] font-bold text-slate-400 dark:text-slate-500 uppercase tracking-widest mb-2">
              Navigation Menu
            </p>
            {navLinks.map((link) => {
              const Icon = link.icon;
              return (
                <NavLink
                  key={link.to}
                  to={link.to}
                  onClick={onClose}
                  className={({ isActive }) => `
                    flex items-center justify-between px-3.5 py-2.5 rounded-lg text-xs font-medium transition-all
                    ${isActive 
                      ? 'bg-sky-600 text-white shadow-md shadow-sky-600/20 font-semibold' 
                      : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100 hover:bg-slate-100 dark:hover:bg-slate-800/60'
                    }
                  `}
                >
                  <div className="flex items-center gap-3">
                    <Icon className="w-4 h-4 shrink-0" />
                    <span>{link.label}</span>
                  </div>
                  {link.badge && (
                    <span className="px-1.5 py-0.5 text-[9px] font-bold bg-amber-500/20 text-amber-600 dark:text-amber-300 rounded border border-amber-500/30 animate-pulse">
                      {link.badge}
                    </span>
                  )}
                </NavLink>
              );
            })}
          </nav>
        </div>

        {/* Lower Info Footer */}
        <div className="p-4 border-t border-slate-200 dark:border-slate-800/80 bg-slate-50/60 dark:bg-slate-950/40 text-[11px] text-slate-500 dark:text-slate-400 space-y-1.5">
          <div className="flex items-center gap-2 text-slate-700 dark:text-slate-300">
            <Building className="w-3.5 h-3.5 text-sky-600 dark:text-sky-400" />
            <span className="font-semibold text-slate-900 dark:text-slate-200">Odisha Demo Portal</span>
          </div>
          <p className="text-[10px] text-slate-500 dark:text-slate-500 leading-tight">
            Khordha District • Tehsil Jatni • BhuNexis Platform
          </p>
        </div>
      </aside>
    </>
  );
}
