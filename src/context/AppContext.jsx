import React, { createContext, useState, useEffect } from 'react';
import { INITIAL_LAND_RECORDS } from '../data/landRecords';
import { INITIAL_AUDIT_EVENTS } from '../data/auditEvents';
import { MOCK_USERS } from '../data/mockUsers';
import { SYSTEM_STATS } from '../data/processingData';

export const AppContext = createContext();

export function AppProvider({ children }) {
  // Land Records State
  const [records, setRecords] = useState(() => {
    try {
      const saved = localStorage.getItem('bhunexis_land_records');
      if (!saved) return INITIAL_LAND_RECORDS;
      const parsed = JSON.parse(saved);
      return parsed.map(rec => {
        const initMatch = INITIAL_LAND_RECORDS.find(i => i.id === rec.id);
        if (initMatch) {
          return { 
            ...rec, 
            citizenId: initMatch.citizenId,
            ownerName: initMatch.ownerName 
          };
        }
        return rec;
      });
    } catch {
      return INITIAL_LAND_RECORDS;
    }
  });

  // Audit Events State
  const [auditEvents, setAuditEvents] = useState(() => {
    try {
      const saved = localStorage.getItem('bhunexis_audit_events');
      return saved ? JSON.parse(saved) : INITIAL_AUDIT_EVENTS;
    } catch {
      return INITIAL_AUDIT_EVENTS;
    }
  });

  // User Management State
  const [userList, setUserList] = useState(() => {
    try {
      const saved = localStorage.getItem('bhunexis_user_list');
      if (!saved) return MOCK_USERS;
      const parsed = JSON.parse(saved);
      if (!parsed.some(u => u.email === 'citizen3@bhoomiai.demo')) {
        return MOCK_USERS;
      }
      return parsed;
    } catch {
      return MOCK_USERS;
    }
  });

  // System Settings State
  const [systemSettings, setSystemSettings] = useState(() => {
    try {
      const saved = localStorage.getItem('bhunexis_system_settings');
      return saved ? JSON.parse(saved) : {
        ocrConfidenceThreshold: 85,
        duplicateDetection: true,
        gisVerification: true,
        autoReviewThreshold: 70,
        auditLogging: true,
        validationRulesCount: 24,
        allowDemoNotifications: true
      };
    } catch {
      return {
        ocrConfidenceThreshold: 85,
        duplicateDetection: true,
        gisVerification: true,
        autoReviewThreshold: 70,
        auditLogging: true,
        validationRulesCount: 24,
        allowDemoNotifications: true
      };
    }
  });

  // Grievances State
  const [grievances, setGrievances] = useState(() => {
    try {
      const saved = localStorage.getItem('bhunexis_grievances');
      return saved ? JSON.parse(saved) : [];
    } catch {
      return [];
    }
  });

  // Persist State Updates to localStorage
  useEffect(() => {
    localStorage.setItem('bhunexis_land_records', JSON.stringify(records));
  }, [records]);

  useEffect(() => {
    localStorage.setItem('bhunexis_audit_events', JSON.stringify(auditEvents));
  }, [auditEvents]);

  useEffect(() => {
    localStorage.setItem('bhunexis_user_list', JSON.stringify(userList));
  }, [userList]);

  useEffect(() => {
    localStorage.setItem('bhunexis_system_settings', JSON.stringify(systemSettings));
  }, [systemSettings]);

  useEffect(() => {
    localStorage.setItem('bhunexis_grievances', JSON.stringify(grievances));
  }, [grievances]);

  // Helper Methods
  const addAuditEvent = (event) => {
    const newEvent = {
      id: `AUD-${Math.floor(100 + Math.random() * 900)}`,
      timestamp: new Date().toLocaleString('en-IN', {
        day: '2-digit', month: 'short', year: 'numeric',
        hour: '2-digit', minute: '2-digit', hour12: true
      }),
      status: 'COMPLETED',
      ipAddress: '10.0.' + Math.floor(Math.random()*10) + '.' + Math.floor(Math.random()*100),
      ...event
    };
    setAuditEvents(prev => [newEvent, ...prev]);
  };

  const addRecord = (newRec, userName = 'Demo Officer') => {
    setRecords(prev => [newRec, ...prev]);
    addAuditEvent({
      userId: 'USR-OFF',
      userName,
      userRole: 'OFFICER',
      action: 'DOCUMENT_UPLOADED',
      actionDisplay: 'Document Upload & Process',
      documentId: newRec.documentId,
      field: 'Verification Status',
      oldValue: null,
      newValue: newRec.verificationStatus
    });
  };

  const updateRecord = (id, updatedFields, reviewerName = 'Demo Reviewer') => {
    setRecords(prev => prev.map(rec => {
      if (rec.id === id) {
        const updated = { ...rec, ...updatedFields };
        return updated;
      }
      return rec;
    }));
  };

  const updateRecordStatus = (id, newStatus, reviewerName = 'Demo Reviewer', conflictReason = null) => {
    setRecords(prev => prev.map(rec => {
      if (rec.id === id) {
        const oldStatus = rec.verificationStatus;
        const updated = {
          ...rec,
          verificationStatus: newStatus,
          verifiedBy: reviewerName,
          verifiedAt: new Date().toLocaleString(),
          conflictDetails: conflictReason || rec.conflictDetails
        };

        addAuditEvent({
          userId: 'USR-REV',
          userName: reviewerName,
          userRole: 'REVIEWER',
          action: newStatus === 'VERIFIED' ? 'RECORD_VERIFIED' : (newStatus === 'REJECTED' ? 'RECORD_REJECTED' : 'CONFLICT_FLAGGED'),
          actionDisplay: `Status set to ${newStatus}`,
          documentId: rec.documentId,
          field: 'Verification Status',
          oldValue: oldStatus,
          newValue: newStatus
        });

        return updated;
      }
      return rec;
    }));
  };

  const updateSettings = (newSettings, adminName = 'Demo Administrator') => {
    setSystemSettings(prev => ({ ...prev, ...newSettings }));
    addAuditEvent({
      userId: 'USR-ADM',
      userName: adminName,
      userRole: 'ADMIN',
      action: 'SETTING_CHANGED',
      actionDisplay: 'System Configuration Updated',
      documentId: 'SYS-CFG',
      field: 'Configuration Parameters',
      oldValue: 'Previous State',
      newValue: 'Updated State'
    });
  };

  const updateUserStatus = (userId, newStatus, adminName = 'Demo Administrator') => {
    setUserList(prev => prev.map(u => {
      if (u.id === userId) {
        const updated = { ...u, status: newStatus };
        addAuditEvent({
          userId: 'USR-ADM',
          userName: adminName,
          userRole: 'ADMIN',
          action: 'USER_MODIFIED',
          actionDisplay: `User account ${newStatus.toLowerCase()}`,
          documentId: u.id,
          field: 'User Status',
          oldValue: u.status,
          newValue: newStatus
        });
        return updated;
      }
      return u;
    }));
  };

  const submitGrievance = (grievanceData) => {
    const newGrievance = {
      id: `GRV-${Date.now()}`,
      createdAt: new Date().toLocaleString(),
      status: 'PENDING',
      ...grievanceData
    };
    setGrievances(prev => [newGrievance, ...prev]);
    addAuditEvent({
      userId: 'USR-CIT',
      userName: grievanceData.contactEmail || 'Citizen User',
      userRole: 'CITIZEN',
      action: 'GRIEVANCE_SUBMITTED',
      actionDisplay: 'Citizen Correction Request',
      documentId: grievanceData.recordId || 'N/A',
      field: grievanceData.issueType,
      oldValue: null,
      newValue: grievanceData.description
    });
  };

  return (
    <AppContext.Provider value={{
      records,
      auditEvents,
      userList,
      systemSettings,
      grievances,
      systemStats: SYSTEM_STATS,
      addRecord,
      updateRecord,
      updateRecordStatus,
      updateSettings,
      updateUserStatus,
      submitGrievance
    }}>
      {children}
    </AppContext.Provider>
  );
}
