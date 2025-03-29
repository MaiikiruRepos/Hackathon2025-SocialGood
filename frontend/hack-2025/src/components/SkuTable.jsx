import React, { useMemo, useState } from 'react';
import {
  useReactTable,
  getCoreRowModel,
  flexRender,
  getFilteredRowModel,
  getPaginationRowModel,
} from '@tanstack/react-table';

const SkuTable = ({ rawData }) => {
  // flatten data for tanstack tables
  const transformData = (data) => {
    const result = [];

    for (const plantId in data.plant) {
      const skuList = data.plant[plantId].sku;
      for (const skuId in skuList) {
        const sku = skuList[skuId];
        result.push({
          plantId,
          skuId,
          description: sku.Description,
          carbon: sku.CarbonLB,
          water: sku.WaterGal,
        });
      }
    }

    return result;
  };

  const data = useMemo(() => transformData(rawData), [rawData]);

  const columns = useMemo(
    () => [
      { header: 'Plant ID', accessorKey: 'plantId', meta: { filterVariant: "text" } },
      { header: 'SKU ID', accessorKey: 'skuId', meta: { filterVariant: "text" } },
      { header: 'Description', accessorKey: 'description', meta: { filterVariant: "text" } },
      { header: 'Carbon (LB)', accessorKey: 'carbon', meta: { filterVariant: "range" } },
      { header: 'Water (Gal)', accessorKey: 'water', meta: { filterVariant: "range" } },
    ],
    []
  );

  const [columnFilters, setColumnFilters] = useState([]);

  const table = useReactTable({
    data,
    columns,
    state: {
      columnFilters,
    },
    onColumnFiltersChange: setColumnFilters,
    getCoreRowModel: getCoreRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    getPaginationRowModel: getPaginationRowModel(), // Added pagination support
  });

  return (
    <div className="w-full max-w-6xl mx-auto px-4 py-10">
      <h2 className="text-2xl font-bold mb-4">SKU List</h2>

      <div className="overflow-x-auto rounded-lg shadow-md border">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            {table.getHeaderGroups().map(headerGroup => (
              <tr key={headerGroup.id}>
                {headerGroup.headers.map(header => (
                  <th
                    key={header.id}
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    {flexRender(header.column.columnDef.header, header.getContext())}
                    {header.column.getCanFilter() ? (
                      <div className="mt-1">
                        <Filter column={header.column} />
                      </div>
                    ) : null}
                  </th>
                ))}
              </tr>
            ))}
          </thead>

          <tbody className="bg-white divide-y divide-gray-200">
            {table.getRowModel().rows.map(row => (
              <tr key={row.id}>
                {row.getVisibleCells().map(cell => (
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
    </div>
  );
};

export default SkuTable;

function Filter({ column }) {
  const columnFilterValue = column.getFilterValue();
  const { filterVariant } = column.columnDef.meta ?? {};

  return filterVariant === 'range' ? (
    <div className="flex space-x-1">
      <input
        type="number"
        value={columnFilterValue?.[0] ?? ''}
        onChange={(e) =>
          column.setFilterValue((old = []) => [e.target.value, old?.[1]])
        }
        placeholder="Min"
        className="w-20 p-1 border rounded"
      />
      <input
        type="number"
        value={columnFilterValue?.[1] ?? ''}
        onChange={(e) =>
          column.setFilterValue((old = []) => [old?.[0], e.target.value])
        }
        placeholder="Max"
        className="w-20 p-1 border rounded"
      />
    </div>
  ) : (
    <input
      type="text"
      value={columnFilterValue ?? ''}
      onChange={(e) => column.setFilterValue(e.target.value)}
      placeholder="Search..."
      className="w-36 p-1 border rounded"
    />
  );
}
