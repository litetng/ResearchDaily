import streamlit as st
import database as db
import fetcher

# 尝试导入 AI 总结模块（Step 5 中会真正实现，目前用占位符）
try:
    from summarizer import summarize_abstract
except ImportError:
    def summarize_abstract(abstract):
        return "⚠️ 本地大模型API模块(summarizer)暂缺，请等待下个步骤 (Step 5) 完成后再使用此功能。"

st.set_page_config(page_title="MyResearchDaily", page_icon="📚", layout="wide")

def init_app():
    db.init_db()

def display_paper_card(paper, tab_identifier):
    paper_id = paper['id']
    # 提取关键字标签
    keyword_badge = f" 🏷️[{paper['keyword']}]" if paper.get('keyword') else ""
    
    # 使用 st.expander 实现卡片式折叠布局
    with st.expander(f"📄 [{paper['published_date']}]{keyword_badge} {paper['title']}", expanded=False):
        st.markdown(f"**📝 Authors:** {paper['authors']}")
        st.markdown(f"**🔗 URL:** [ArXiv Link]({paper['url']})")
        st.markdown(f"**📖 Abstract:**\n{paper['abstract']}")

        # 🤖 AI 总结按钮，按需调用大模型
        if st.button("🤖 AI 总结核心创新点", key=f"btn_ai_{paper_id}_{tab_identifier}"):
            with st.spinner("正在调用 AI 模型生成总结..."):
                summary = summarize_abstract(paper['abstract'])
                st.info(f"**核心创新点：** {summary}")
        
        st.divider()
        
        # 互动与批注组件
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            # 状态切换: 当前状态是不是“已读”
            current_status = paper.get('status', '未读')
            is_read = (current_status == '已读')
            new_is_read = st.checkbox("标为已读", value=is_read, key=f"chk_{paper_id}_{tab_identifier}")
            new_status_str = '已读' if new_is_read else '未读'
        
        with col2:
            # 重要等级下拉菜单（星级）
            current_importance = paper.get('importance_level', 1)
            importance = st.selectbox(
                "重要等级", 
                options=[1, 2, 3, 4, 5], 
                index=current_importance - 1, 
                format_func=lambda x: "🌟" * x,
                key=f"star_{paper_id}_{tab_identifier}"
            )
            
        with col3:
            # 个人批注
            current_notes = paper.get('user_notes', '')
            notes = st.text_area("📝 个人批注", value=current_notes, height=68, key=f"note_{paper_id}_{tab_identifier}")
        
        # 保存此论文的状态到本地 SQLite，待用户主动点击时才发生落库
        if st.button("💾 保存/更新状态", key=f"btn_save_{paper_id}_{tab_identifier}"):
            # 先确保存在记录（如果是今日查新刚刷出来的临时数据，则会 INSERT 缺省初始数据）
            db.save_paper(paper)
            # 再更新为用户刚指定的最新字段
            db.update_paper(paper_id, new_status_str, importance, notes)
            st.toast(f"✅ 保存成功: {paper['title'][:20]}...")
            # 重新渲染页面以刷新 Tab 数据
            st.rerun()

def main():
    init_app()
    
    st.title("📚 MyResearchDaily")
    st.markdown("💡 每天一点点，跟踪最新的学术动态——你的轻量级本地论文管理器。")
    
    # 左侧边栏：关键词配置
    with st.sidebar:
        st.header("⚙️ 查新设置")
        st.markdown("自定义要抓取的关键词（每行一个）：")
        user_keywords_str = st.text_area("关键词列表", value="\n".join(fetcher.DEFAULT_KEYWORDS), height=150)
        custom_keywords = [k.strip() for k in user_keywords_str.split('\n') if k.strip()]
        st.markdown("---")
        # 解除强制 3 篇的限制，提供给用户高度自由的滑动条调整
        max_articles = st.slider("每个关键词拉取篇数", min_value=1, max_value=50, value=10)
        st.caption("提示：ArXiv API 对高频访问有限制，建议保留核心关键字。")

    # 构建三大模块的 Tab
    tab1, tab2, tab3 = st.tabs(["🆕 今日查新", "📖 未读列表", "🗄️ 已读归档"])
    
    with tab1:
        st.subheader("抓取最新的学术前沿")
        st.markdown("通过左侧自定义的关键词自动检索最新发表文章。")
        
        if st.button("🔄 开始抓取近况", use_container_width=True):
            with st.spinner("⏳ 正在请求 ArXiv 抓取最新论文数据（可能需要几秒钟）..."):
                fetched_papers = fetcher.fetch_all_papers(keywords=custom_keywords, max_results_per_keyword=max_articles)
                st.session_state['fetched_papers'] = fetched_papers
                st.success(f"🎉 抓取完成！共找到 {len(fetched_papers)} 篇临时拉取的论文供您筛选。")
                
        # 缓存于 session_state 这样切换组件不丢失
        if 'fetched_papers' in st.session_state:
            for idx, p in enumerate(st.session_state['fetched_papers']):
                display_paper_card(p, f"tab1_{idx}")
                
    with tab2:
        st.subheader("需要跟进的未读论文")
        unread_papers = db.get_papers_by_status("未读")
        if not unread_papers:
            st.info("☕ 恭喜你，列表空空如也！目前没有未读文章。")
        else:
            for p in unread_papers:
                display_paper_card(p, "tab2")
            
    with tab3:
        st.subheader("已经沉淀的学术财富")
        read_papers = db.get_papers_by_status("已读")
        if not read_papers:
            st.info("📦 您还没有已读完毕并归档的论文。")
        else:
            for p in read_papers:
                display_paper_card(p, "tab3")

if __name__ == "__main__":
    main()
