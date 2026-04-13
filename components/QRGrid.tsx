/** @jsxImportSource theme-ui */
import { QRCodeSVG } from 'qrcode.react';

export interface QRGridItem {
  url: string;
  label: string;
}

export interface QRGridProps {
  items: QRGridItem[];
}

export function QRGrid({ items }: QRGridProps) {
  return (
    <div
      sx={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))',
        gap: 5,
        maxWidth: 960,
        mx: 'auto',
        py: 4,
        justifyItems: 'center',
      }}
    >
      {items.map((item) => (
        <div
          key={item.url}
          sx={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            gap: 2,
          }}
        >
          <div
            sx={{
              bg: '#ffffff',
              p: 2,
              borderRadius: 6,
            }}
          >
            <QRCodeSVG value={item.url} size={148} fgColor="#3b1e1c" bgColor="#ffffff" level="M" />
          </div>
          <span
            sx={{
              fontFamily: 'monospace',
              fontSize: 1,
              color: 'text',
              textAlign: 'center',
              opacity: 0.85,
            }}
          >
            {item.label}
          </span>
        </div>
      ))}
    </div>
  );
}
