import React, { useState } from "react";

function App() {
  const [patient, setPatient] = useState({ name: "", age: 0 });
  const [toothEntry, setToothEntry] = useState({ tooth_number: 0, pocket_depth_mm: 0 });

  return (
    <div style={{ padding: "40px", fontFamily: "sans-serif" }}>
      <h2>Patient Entry</h2>
      <div>
        <label>Name: </label>
        <input
          type="text"
          value={patient.name}
          onChange={(e) => setPatient({ ...patient, name: e.target.value })}
        />
      </div>
      <div>
        <label>Age: </label>
        <input
          type="number"
          value={patient.age}
          onChange={(e) => setPatient({ ...patient, age: parseInt(e.target.value) || 0 })}
        />
      </div>

      <h3>Tooth Entry</h3>
      <div>
        <label>Tooth #: </label>
        <input
          type="number"
          value={toothEntry.tooth_number}
          onChange={(e) => setToothEntry({ ...toothEntry, tooth_number: parseInt(e.target.value) || 0 })}
        />
      </div>
      <div>
        <label>Pocket (mm): </label>
        <input
          type="number"
          value={toothEntry.pocket_depth_mm}
          onChange={(e) =>
            setToothEntry({
              ...toothEntry,
              pocket_depth_mm: parseFloat(e.target.value) || 0,
            })
          }
        />
      </div>
    </div>
  );
}

export default App;
