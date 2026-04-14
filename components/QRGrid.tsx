/** @jsxImportSource theme-ui */
import { QRCodeSVG } from 'qrcode.react';

export interface QRGridItem {
  url: string;
  label: string;
}

export interface QRGridProps {
  items: QRGridItem[];
  layout?: 'auto' | 'row';
  size?: number;
}

function QRCard({ item, size }: { item: QRGridItem; size: number }) {
  return (
    <div
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: 3,
      }}
    >
      <div
        sx={{
          bg: '#ffffff',
          p: 3,
          borderRadius: 8,
        }}
      >
        <QRCodeSVG value={item.url} size={size} fgColor="#3b1e1c" bgColor="#ffffff" level="M" />
      </div>
      <span
        sx={{
          fontFamily: 'monospace',
          fontSize: 2,
          color: 'text',
          textAlign: 'center',
          opacity: 0.85,
        }}
      >
        {item.label}
      </span>
    </div>
  );
}

export function QRGrid({ items, layout = 'auto', size = 200 }: QRGridProps) {
  if (layout === 'row') {
    return (
      <div
        sx={{
          display: 'flex',
          flexDirection: 'row',
          alignItems: 'flex-start',
          justifyContent: 'center',
          py: 4,
          flexWrap: ['wrap', 'nowrap'],
          gap: [4, 5],
        }}
      >
        {items.map((item) => (
          <QRCard key={item.url} item={item} size={size} />
        ))}
      </div>
    );
  }

  // Split into rows: first 2, then remaining
  const topRow = items.slice(0, 2);
  const bottomRow = items.slice(2);

  return (
    <div
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: 5,
        py: 4,
      }}
    >
      {/* Top row: 2 items */}
      <div
        sx={{
          display: 'flex',
          gap: 6,
          justifyContent: 'center',
        }}
      >
        {topRow.map((item) => (
          <QRCard key={item.url} item={item} size={size} />
        ))}
      </div>
      {/* Bottom row: 3 items */}
      {bottomRow.length > 0 && (
        <div
          sx={{
            display: 'flex',
            gap: 6,
            justifyContent: 'center',
          }}
        >
          {bottomRow.map((item) => (
            <QRCard key={item.url} item={item} size={size} />
          ))}
        </div>
      )}
    </div>
  );
}
