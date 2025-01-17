# Đờn-bà AI Chatbot

[**Đờn-bà AI Chatbot**](https://nghechuongnugioi.nghiencuuvietnam.com) là một chatbot trí tuệ nhân tạo được thiết kế để tái hiện phong cách ngôn ngữ và quan điểm của các nữ nhà văn từ *Nữ Giới Chung* (Chuông Phụ Nữ), một tờ báo của Việt Nam từ năm 1918. Dự án này kết hợp việc bảo tồn lịch sử với công nghệ AI tiên tiến, đảm bảo tính chính xác, bối cảnh văn hóa và tương tác hấp dẫn.

## Tính năng nổi bật

- **Dữ liệu chân thực**: Được xây dựng từ nội dung OCR của 20 tập *Nữ Giới Chung*, đảm bảo độ chính xác về ngôn ngữ và lịch sử.
- **Phong cách ngôn ngữ lịch sử**: Mô phỏng giọng văn và phong cách viết của các nữ nhà văn Việt Nam đầu thế kỷ 20.
- **Tích hợp AI tiên tiến**:
  - Ban đầu triển khai với Gemini Pro để tạo phản hồi nhanh và chính xác về ngôn ngữ.
  - Nâng cấp với Retrieval-Augmented Generation (RAG) để trả lời dựa trên dữ liệu thực tế và bối cảnh chính xác.
  - Sử dụng GPT-4o để tăng cường sự tự nhiên và phù hợp về văn hóa.

## Phương pháp tiếp cận

1. **Chuẩn bị dữ liệu**:
   - Sử dụng OCR với ClaudeAI để số hóa tài liệu lịch sử một cách hiệu quả.
   - Dữ liệu được tổ chức có hệ thống, bao gồm trích dẫn, ngày xuất bản và thông tin tác giả, đảm bảo phản hồi có căn cứ từ nội dung lịch sử.

2. **Triển khai mô hình**:
   - Phản hồi ngôn ngữ ban đầu được cung cấp bởi Gemini Pro, tái hiện phong cách ngôn ngữ.
   - Chuyển sang RAG với LangChain, embedding của OpenAI và cơ sở dữ liệu Chroma để đảm bảo phản hồi chính xác và có nguồn dẫn.

3. **Tối ưu hóa chi phí**:
   - Cân bằng hiệu năng và chi phí thông qua các chiến lược API và embedding chọn lọc.

## Ứng dụng

Chatbot này mang lại một công cụ tương tác thú vị cho:
- Khám phá tư tưởng nữ quyền sớm và quan điểm lịch sử về quyền phụ nữ tại Việt Nam.
- Các sáng kiến bảo tồn văn hóa và giáo dục.
- Trải nghiệm học tập tương tác về lịch sử và văn học Việt Nam.

## Tham khảo

- [Lưu trữ Nữ Giới Chung](https://ngcai.nghiencuuvietnam.com/)
- [Hướng dẫn LangChain RAG](https://github.com/pixegami/langchain-rag-tutorial)

---

# Đờn-bà AI Chatbot

The **Đờn-bà AI Chatbot** is an AI-powered chatbot designed to replicate the linguistic style and perspectives of female writers from *Nữ Giới Chung* (Women’s Bell), a Vietnamese newspaper from 1918. This project combines historical preservation with cutting-edge AI technology, ensuring accuracy, cultural context, and engaging interactions.

## Key Features

- **Authentic Data**: Built on OCR-processed content from 20 volumes of *Nữ Giới Chung*, ensuring linguistic and historical accuracy.
- **Historical Language Style**: Mimics the tone and writing style of early 20th-century Vietnamese female writers.
- **Advanced AI Integration**:
  - Initial implementation using Gemini Pro for fast, linguistically accurate responses.
  - Enhanced with Retrieval-Augmented Generation (RAG) for fact-based, contextually precise answers.
  - Powered by GPT-4o for fluency and cultural relevance.

## Methodology

1. **Data Preparation**:
   - OCR processing with ClaudeAI to efficiently digitize historical documents.
   - Organized dataset structure, including quotes, publication dates, and author details, to ground responses in authentic historical content.

2. **Model Implementation**:
   - Initial generative responses powered by Gemini Pro, capturing linguistic nuances.
   - Transitioned to RAG using LangChain, OpenAI embeddings, and Chroma database for accurate, source-cited answers.

3. **Cost Optimization**:
   - Balancing performance and affordability through selective API and embedding strategies.

## Applications

This chatbot offers an engaging tool for:
- Exploring early feminist thoughts and historical perspectives on women's rights in Vietnam.
- Educational and cultural preservation initiatives.
- Interactive learning experiences focused on Vietnamese history and literature.

## References

- [Nữ Giới Chung Archives](https://ngcai.nghiencuuvietnam.com/)
- [LangChain RAG Tutorial](https://github.com/pixegami/langchain-rag-tutorial)
