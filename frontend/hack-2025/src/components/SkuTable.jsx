import React, { useEffect, useMemo, useState } from 'react';
import {
  useReactTable,
  getCoreRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  flexRender,
} from '@tanstack/react-table';
import axios from 'axios';

// Setup default baseURL (ensure trailing slash)
axios.defaults.baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
axios.defaults.headers.post['Content-Type'] = 'application/json';

const SkuTable = ({ googleID }) => {
  const [rawData, setRawData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [matchedDatabases, setMatchedDatabases] = useState(0);
  const [attemptedDatabases, setAttemptedDatabases] = useState(0);

  useEffect(() => {
    const fetchAndBuildData = async () => {
      if (!googleID) {
        console.warn('⚠️ googleID is undefined — skipping fetch.');
        return;
      }

      console.log(`🔍 Fetching data for GoogleID: ${googleID}`);
      setLoading(true);
      setError(null);
      setRawData([]);
      setMatchedDatabases(0);
      setAttemptedDatabases(0);

      try {
        const tsRes = await axios.post('/get_all_timestamps/', { googleID });
        const timestamps = Array.isArray(tsRes.data?.timestamps)
          ? [...new Set(tsRes.data.timestamps)]
          : [];

        console.log('🕒 Found timestamps:', timestamps);

        if (timestamps.length === 0) {
          console.warn(`⚠️ No timestamps found for GoogleID: ${googleID}`);
          return;
        }

        const combinedResults = [];
        let successCount = 0;
        let attemptedCount = 0;

        for (const timestamp of timestamps) {
          const database = `${googleID}-${timestamp}`;
          console.log(`📦 Fetching from database: ${database}`);
          attemptedCount++;

          try {
            const searchRes = await axios.post('/search_data/', { database });
            console.log(`📨 Raw response from ${database}:`, searchRes.data);

            const dbData = Array.isArray(searchRes.data?.data)
              ? searchRes.data.data
              : [];

            if (dbData.length === 0) {
              console.warn(`ℹ️ No data returned for database: ${database}`);
              continue;
            }

            dbData.forEach((item) => {
              combinedResults.push({
                plant_id: item.plant_id ?? 'N/A',
                sku_id: item.sku_id ?? 'N/A',
                description: item.description ?? item.sku_name ?? 'Unnamed',
                carbon: item.carbon_percent ?? 0,
                water: item.water_percent ?? 0,
                timestamp,
              });
            });

            successCount++;
          } catch (innerErr) {
            console.error(`❌ Failed to load from ${database}:`, innerErr?.response?.data || innerErr.message || innerErr);
          }
        }

        setAttemptedDatabases(attemptedCount);
        setMatchedDatabases(successCount);
        console.log(`✅ Total entries fetched: ${combinedResults.length}`);
        setRawData(combinedResults);
      } catch (err) {
        console.error('❌ Error during timestamp fetch:', err?.response?.data || err.message || err);
        setError('Failed to load data. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchAndBuildData();
  }, [googleID]);

  const columns = useMemo(
    () => [
      { header: 'Plant ID', accessorKey: 'plant_id' },
      { header: 'SKU ID', accessorKey: 'sku_id' },
      { header: 'Description', accessorKey: 'description' },
      { header: 'Carbon (LB)', accessorKey: 'carbon' },
      { header: 'Water (Gal)', accessorKey: 'water' },
      { header: 'Timestamp', accessorKey: 'timestamp' },
    ],
    []
  );

  const table = useReactTable({
    data: rawData,
    columns,
    getCoreRowModel: getCoreRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
  });

  return (
    <div className="w-full max-w-6xl mx-auto px-4 py-10">
      <h2 className="text-2xl font-bold mb-4">SKU List</h2>

      {loading ? (
        <p>Loading...</p>
      ) : error ? (
        <p className="text-red-500">{error}</p>
      ) : rawData.length === 0 ? (
        <div className="text-gray-500">
          <p>
            No SKU data available
            {googleID ? <> for <strong>{googleID}</strong></> : <>.</>}
          </p>
          <p>
            Attempted {attemptedDatabases} timestamp{attemptedDatabases !== 1 ? 's' : ''}, matched {matchedDatabases}.
          </p>
        </div>
      ) : (
        <>
          <p className="mb-4 text-sm text-gray-600">
            Showing data from {matchedDatabases} of {attemptedDatabases} databases.
          </p>

          <div className="overflow-x-auto rounded-lg shadow-md border">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                {table.getHeaderGroups().map((headerGroup) => (
                  <tr key={headerGroup.id}>
                    {headerGroup.headers.map((header) => (
                      <th
                        key={header.id}
                        className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                      >
                        {flexRender(header.column.columnDef.header, header.getContext())}
                      </th>
                    ))}
                  </tr>
                ))}
              </thead>

              <tbody className="bg-white divide-y divide-gray-200">
                {table.getRowModel().rows.map((row) => (
                  <tr key={row.id}>
                    {row.getVisibleCells().map((cell) => (
                      <td
                        key={cell.id}
                        className="px-6 py-4 whitespace-nowrap text-sm text-gray-700"
                      >
                        {flexRender(cell.column.columnDef.cell, cell.getContext())}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}
    </div>
  );
};

export default SkuTable;
