// CADASTRAL PARCEL GEOJSON DATA — Jatni, Khordha, Odisha Demo Center (20.1824° N, 85.7356° E)

export const DEMO_MAP_PARCELS = {
  type: "FeatureCollection",
  features: [
    {
      type: "Feature",
      id: "PARCEL-101",
      properties: {
        parcelId: "PARCEL-101",
        recordId: "LR-2026-001",
        citizenId: "CIT001",
        surveyNumber: "125/3",
        khataNumber: "87",
        ownerName: "Ramesh Chandra Patnaik",
        area: "2.45 Acres",
        village: "BhuNexis Demo Village",
        tehsil: "Jatni",
        district: "Khordha",
        landClassification: "Agricultural (Rayati)",
        verificationStatus: "VERIFIED"
      },
      geometry: {
        type: "Polygon",
        coordinates: [
          [
            [85.7340, 20.1820],
            [85.7355, 20.1820],
            [85.7358, 20.1832],
            [85.7342, 20.1833],
            [85.7340, 20.1820]
          ]
        ]
      }
    },
    {
      type: "Feature",
      id: "PARCEL-102",
      properties: {
        parcelId: "PARCEL-102",
        recordId: "LR-2026-002",
        citizenId: "CIT002",
        surveyNumber: "118/2",
        khataNumber: "64",
        ownerName: "Sanjay Kumar Swain",
        area: "1.82 Acres",
        village: "Shantipur Mouza",
        tehsil: "Jatni",
        district: "Khordha",
        landClassification: "Homestead (Gharabari)",
        verificationStatus: "UNDER REVIEW"
      },
      geometry: {
        type: "Polygon",
        coordinates: [
          [
            [85.7358, 20.1820],
            [85.7370, 20.1820],
            [85.7372, 20.1830],
            [85.7358, 20.1832],
            [85.7358, 20.1820]
          ]
        ]
      }
    },
    {
      type: "Feature",
      id: "PARCEL-103",
      properties: {
        parcelId: "PARCEL-103",
        recordId: "LR-2026-003",
        citizenId: "CIT004",
        surveyNumber: "203/7",
        khataNumber: "112",
        ownerName: "Anusaya Mohanty",
        area: "3.14 Acres",
        village: "Haripur Mouza",
        tehsil: "Jatni",
        district: "Khordha",
        landClassification: "Agricultural (Irrigated)",
        verificationStatus: "LOW CONFIDENCE"
      },
      geometry: {
        type: "Polygon",
        coordinates: [
          [
            [85.7372, 20.1820],
            [85.7390, 20.1820],
            [85.7392, 20.1835],
            [85.7372, 20.1830],
            [85.7372, 20.1820]
          ]
        ]
      }
    },
    {
      type: "Feature",
      id: "PARCEL-104",
      properties: {
        parcelId: "PARCEL-104",
        recordId: "LR-2026-004",
        citizenId: "CIT001",
        surveyNumber: "89/1",
        khataNumber: "45",
        ownerName: "Ramesh Chandra Patnaik",
        area: "0.95 Acres",
        village: "BhuNexis Demo Village",
        tehsil: "Jatni",
        district: "Khordha",
        landClassification: "Commercial Plot",
        verificationStatus: "CONFLICT"
      },
      geometry: {
        type: "Polygon",
        coordinates: [
          [
            [85.7340, 20.1833],
            [85.7358, 20.1832],
            [85.7360, 20.1845],
            [85.7342, 20.1846],
            [85.7340, 20.1833]
          ]
        ]
      }
    },
    {
      type: "Feature",
      id: "PARCEL-105",
      properties: {
        parcelId: "PARCEL-105",
        recordId: "LR-2026-005",
        citizenId: "CIT004",
        surveyNumber: "142/4",
        khataNumber: "105",
        ownerName: "Anusaya Mohanty",
        area: "4.50 Acres",
        village: "Ratanpur Mouza",
        tehsil: "Jatni",
        district: "Khordha",
        landClassification: "Agricultural (Rayati)",
        verificationStatus: "VERIFIED"
      },
      geometry: {
        type: "Polygon",
        coordinates: [
          [
            [85.7360, 20.1832],
            [85.7372, 20.1830],
            [85.7375, 20.1848],
            [85.7360, 20.1845],
            [85.7360, 20.1832]
          ]
        ]
      }
    },
    {
      type: "Feature",
      id: "PARCEL-106",
      properties: {
        parcelId: "PARCEL-106",
        recordId: "LR-2026-006",
        citizenId: "CIT004",
        surveyNumber: "76/3",
        khataNumber: "32",
        ownerName: "Subhashree Jena",
        area: "1.20 Acres",
        village: "BhuNexis Demo Village",
        tehsil: "Jatni",
        district: "Khordha",
        landClassification: "Homestead (Gharabari)",
        verificationStatus: "EXTRACTED"
      },
      geometry: {
        type: "Polygon",
        coordinates: [
          [
            [85.7372, 20.1830],
            [85.7392, 20.1835],
            [85.7395, 20.1850],
            [85.7375, 20.1848],
            [85.7372, 20.1830]
          ]
        ]
      }
    },
    {
      type: "Feature",
      id: "PARCEL-107",
      properties: {
        parcelId: "PARCEL-107",
        recordId: "LR-2026-007",
        citizenId: "CIT005",
        surveyNumber: "310/1",
        khataNumber: "158",
        ownerName: "Debasis Tripathy",
        area: "5.60 Acres",
        village: "Shantipur Mouza",
        tehsil: "Jatni",
        district: "Khordha",
        landClassification: "Orchard (Bagayat)",
        verificationStatus: "VERIFIED"
      },
      geometry: {
        type: "Polygon",
        coordinates: [
          [
            [85.7342, 20.1846],
            [85.7360, 20.1845],
            [85.7362, 20.1860],
            [85.7344, 20.1861],
            [85.7342, 20.1846]
          ]
        ]
      }
    }
  ]
};
