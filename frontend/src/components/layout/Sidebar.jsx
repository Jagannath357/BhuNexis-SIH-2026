import React from 'react';
import { NavLink } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import {
  LayoutDashboard,
  FileUp,
  MapPin,
  User,
  Users,
  Settings,
  CheckSquare,
  ShieldCheck,
  Search,
  FileText,
  HelpCircle
} from 'lucide-react';

export default function Sidebar() {
  const { role } = useAuth();

  const getDashboardLink = () => {
    switch (role) {
      case 'ADMIN': return '/a/dashboard';
      case 'OFFICER': return '/o/dashboard';
      case 'REVIEWER': return '/r/dashboard';
      case 'AUDITOR': return '/au/dashboard';
      case 'CITIZEN': return '/u/dashboard';
      default: return '/u/dashboard';
    }
  };

  return (
    <aside className="w-64 bg-[var(--bg-sidebar)] text-[var(--text-sidebar)] flex flex-col h-screen sticky top-0 border-r border-slate-800 shadow-xl transition-colors">
      {/* Brand Header */}
      <div className="p-5 border-b border-slate-800 flex items-center space-x-3">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-500 to-teal-400 flex items-center justify-center font-bold text-white text-xl shadow-lg shadow-emerald-500/20">
          BN
        </div>
        <div>
          <h1 className="font-bold text-lg tracking-tight text-white">BhuNexis</h1>
          <p className="text-xs text-emerald-400 font-medium tracking-wide">Land Records AI Platform</p>
        </div>
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 px-3 py-4 space-y-1.5 overflow-y-auto">
        <NavLink
          to={getDashboardLink()}
          className={({ isActive }) =>
            `flex items-center space-x-3 px-3.5 py-2.5 rounded-lg text-sm font-medium transition-all ${
              isActive
                ? 'bg-emerald-600 text-white shadow-md shadow-emerald-600/30'
                : 'text-slate-300 hover:bg-slate-800/60 hover:text-white'
            }`
          }
        >
          <LayoutDashboard className="w-5 h-5 text-emerald-400" />
          <span>Dashboard</span>
        </NavLink>

        {/* Officer & Admin Ingestion */}
        {(role === 'OFFICER' || role === 'ADMIN') && (
          <NavLink
            to="/o/upload"
            className={({ isActive }) =>
              `flex items-center space-x-3 px-3.5 py-2.5 rounded-lg text-sm font-medium transition-all ${
                isActive
                  ? 'bg-emerald-600 text-white shadow-md shadow-emerald-600/30'
                  : 'text-slate-300 hover:bg-slate-800/60 hover:text-white'
              }`
            }
          >
            <FileUp className="w-5 h-5 text-teal-400" />
            <span>Upload Land Record</span>
          </NavLink>
        )}

        {/* Reviewer Queue */}
        {(role === 'REVIEWER' || role === 'ADMIN') && (
          <NavLink
            to="/r/review"
            className={({ isActive }) =>
              `flex items-center space-x-3 px-3.5 py-2.5 rounded-lg text-sm font-medium transition-all ${
                isActive
                  ? 'bg-emerald-600 text-white shadow-md shadow-emerald-600/30'
                  : 'text-slate-300 hover:bg-slate-800/60 hover:text-white'
              }`
            }
          >
            <CheckSquare className="w-5 h-5 text-amber-400" />
            <span>Human Review Queue</span>
          </NavLink>
        )}

        {/* Auditor Logs */}
        {(role === 'AUDITOR' || role === 'ADMIN') && (
          <NavLink
            to="/au/audit"
            className={({ isActive }) =>
              `flex items-center space-x-3 px-3.5 py-2.5 rounded-lg text-sm font-medium transition-all ${
                isActive
                  ? 'bg-emerald-600 text-white shadow-md shadow-emerald-600/30'
                  : 'text-slate-300 hover:bg-slate-800/60 hover:text-white'
              }`
            }
          >
            <ShieldCheck className="w-5 h-5 text-cyan-400" />
            <span>Audit History</span>
          </NavLink>
        )}

        {/* Admin Options */}
        {role === 'ADMIN' && (
          <>
            <div className="pt-3 pb-1 px-3.5 text-xs font-semibold uppercase tracking-wider text-slate-500">
              Administration
            </div>
            <NavLink
              to="/a/users"
              className={({ isActive }) =>
                `flex items-center space-x-3 px-3.5 py-2.5 rounded-lg text-sm font-medium transition-all ${
                  isActive
                    ? 'bg-emerald-600 text-white shadow-md shadow-emerald-600/30'
                    : 'text-slate-300 hover:bg-slate-800/60 hover:text-white'
                }`
              }
            >
              <Users className="w-5 h-5 text-indigo-400" />
              <span>User Management</span>
            </NavLink>
            <NavLink
              to="/a/settings"
              className={({ isActive }) =>
                `flex items-center space-x-3 px-3.5 py-2.5 rounded-lg text-sm font-medium transition-all ${
                  isActive
                    ? 'bg-emerald-600 text-white shadow-md shadow-emerald-600/30'
                    : 'text-slate-300 hover:bg-slate-800/60 hover:text-white'
                }`
              }
            >
              <Settings className="w-5 h-5 text-slate-400" />
              <span>System Settings</span>
            </NavLink>
          </>
        )}

        {/* Citizen Links */}
        {role === 'CITIZEN' && (
          <>
            <NavLink
              to="/u/search"
              className={({ isActive }) =>
                `flex items-center space-x-3 px-3.5 py-2.5 rounded-lg text-sm font-medium transition-all ${
                  isActive
                    ? 'bg-emerald-600 text-white shadow-md shadow-emerald-600/30'
                    : 'text-slate-300 hover:bg-slate-800/60 hover:text-white'
                }`
              }
            >
              <Search className="w-5 h-5 text-blue-400" />
              <span>Search Verified Records</span>
            </NavLink>
          </>
        )}

        {/* GIS Map View - Available for all */}
        <NavLink
          to="/map"
          className={({ isActive }) =>
            `flex items-center space-x-3 px-3.5 py-2.5 rounded-lg text-sm font-medium transition-all ${
              isActive
                ? 'bg-emerald-600 text-white shadow-md shadow-emerald-600/30'
                : 'text-slate-300 hover:bg-slate-800/60 hover:text-white'
            }`
          }
        >
          <MapPin className="w-5 h-5 text-emerald-400" />
          <span>GIS Map View</span>
        </NavLink>

        {/* User Profile */}
        <NavLink
          to="/profile"
          className={({ isActive }) =>
            `flex items-center space-x-3 px-3.5 py-2.5 rounded-lg text-sm font-medium transition-all ${
              isActive
                ? 'bg-emerald-600 text-white shadow-md shadow-emerald-600/30'
                : 'text-slate-300 hover:bg-slate-800/60 hover:text-white'
            }`
          }
        >
          <User className="w-5 h-5 text-sky-400" />
          <span>My Profile</span>
        </NavLink>
      </nav>

      {/* Role Badge Footer */}
      <div className="p-4 border-t border-slate-800 bg-slate-900/50">
        <div className="flex items-center justify-between text-xs">
          <span className="text-slate-400">Current Role</span>
          <span className="px-2 py-0.5 rounded font-semibold bg-emerald-950 text-emerald-300 border border-emerald-800">
            {role}
          </span>
        </div>
      </div>
    </aside>
  );
}
