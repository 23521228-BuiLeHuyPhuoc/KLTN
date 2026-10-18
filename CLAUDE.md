# Hướng dẫn cho Claude

## Giao việc cho subagent

Dự án có ba subagent trong `.claude/agents/`, chọn theo độ khó của việc:

- `architect` (Opus): việc khó, phức tạp - thiết kế phương pháp, lên kế hoạch thực nghiệm, phân tích bug khó, đối chiếu với đề cương.
- `coder` (Sonnet): viết, sửa, refactor code và test khi yêu cầu đã rõ.
- `helper` (Haiku): việc vặt - tìm tệp, đọc/tóm tắt, tra cứu, đổi tên, format.

Khi một yêu cầu gồm nhiều phần, chia ra và giao từng phần cho đúng agent. Việc chỉ cần một hai lệnh thì tự làm, không cần gọi agent.

## Quy ước

- Không đọc hay in nội dung `.env`.
- Trả lời bằng tiếng Việt.
