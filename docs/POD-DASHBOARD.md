# POD Dashboard 사용 가이드

## 1) 목적
`pod.html`은 Shopify + Etsy 병행 운영 POD(Print-on-Demand) 스토어를 위한 운영 모니터링 화면입니다.

핵심 섹션:
- Overview
- Orders
- Profit
- Channel Mix
- Automation Status
- Alerts

## 2) 실행 방법
- 브라우저에서 `http://localhost:8088/zoe-dashboard/pod.html` 또는 배포 경로의 `/zoe-dashboard/pod.html` 접속
- 상단 `Mock 새로고침` 버튼으로 mock 데이터 변동 확인

## 3) 현재 데이터 구조(mock)
`pod.html` 내부 `mock` 객체를 사용합니다.

```js
{
  totalOrders7d,
  openOrders,
  revenue,
  cogs,
  fees,
  netProfit,
  channelMix: { shopify, etsy },
  automationRate,
  alertsCount,
  orders: [{ id, channel, status, eta }],
  automation: [string],
  alerts: [string]
}
```

## 4) 확장 포인트(실데이터 연동)
1. `mock`을 제거하고 `fetch('/api/pod/summary')` 방식으로 교체
2. 채널별 원본 API 응답을 서버에서 정규화 후 전달
3. 필수 API 엔드포인트 예시
   - `/api/pod/orders?channel=shopify|etsy`
   - `/api/pod/profit?range=7d`
   - `/api/pod/automation-status`
   - `/api/pod/alerts`
4. 웹훅 기반 업데이트 시 클라이언트 polling(30~60초) 또는 SSE 적용

## 5) Shopify + Etsy 병행 운영 관점 체크포인트
- SKU/Variant 매핑 테이블을 단일 기준으로 유지
- Etsy 주문과 Shopify 주문의 상태값을 공통 상태로 정규화
- 수수료 체계가 다르므로 순이익 계산 로직을 채널별로 분리
- 주문 소스 채널과 Printify 주문 ID를 반드시 1:1 추적 가능하게 저장
