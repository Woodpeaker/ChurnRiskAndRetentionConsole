import React, { useEffect, useState } from 'react'
import EnhancedTable from './Components/EnhancedTable'
import CustomStepper from './Components/CustomStepper'

const headCells = [
    {
        id: 'customer_id',
        numeric: false,
        disablePadding: true,
        label: 'Customer ID',
    },
    {
        id: 'tenure',
        numeric: true,
        disablePadding: false,
        label: 'Tenure',
    },
    {
        id: 'monthly_charges',
        numeric: true,
        disablePadding: false,
        label: 'Monthly Charges',
    },
    {
        id: 'churn',
        numeric: false,
        disablePadding: false,
        label: 'Churn',
    },
    {
        id: 'risk_score',
        numeric: true,
        disablePadding: false,
        label: 'Risk Score',
    },
];
function App() {
    const [records, setRecords] = useState([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        async function load() {
            try {

                const r = await fetch('/customers')
                const rj = await r.json()
                setRecords(rj)
            } catch (err) {
                console.error(err)
            } finally {
                setLoading(false)
            }
        }
        load()
    }, [])

    return (
        <div className="app">
            <header>
                <h1>Customer Records</h1>
            </header>
            {loading ? (
                <p>Loading…</p>
            ) : (
                <main>

                    <h2>Risk Score Rules</h2>
                    <CustomStepper />
                    <h2>Table Content</h2>
                    <EnhancedTable headCells={headCells} rows={records} ModalEnabled={true} />
                </main>
            )}
        </div>
    )
}

export default App
