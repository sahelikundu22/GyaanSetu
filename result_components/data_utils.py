from collections import defaultdict

def organize_data(subject_data_raw):
    """Organize raw data into subject-wise and chapter-wise structures"""
    subject_wise_data = defaultdict(list)
    chapter_wise_data = defaultdict(lambda: defaultdict(list))
    
    for subject, chapter, score, total in subject_data_raw:
        subject_wise_data[subject].append((score, total))
        chapter_wise_data[subject][chapter].append((score, total))
    
    return subject_wise_data, chapter_wise_data

def calculate_subject_stats(subject_wise_data):
    """Calculate statistics for all subjects"""
    subject_summary = []
    for subject, attempts in subject_wise_data.items():
        total_score = sum(s for s, t in attempts)
        total_questions = sum(t for s, t in attempts)
        accuracy = (total_score / total_questions * 100) if total_questions > 0 else 0
        attempts_count = len(attempts)
        
        subject_summary.append({
            "Subject": subject,
            "Attempts": attempts_count,
            "Accuracy": f"{accuracy:.1f}%",
            "Questions": f"{total_score}/{total_questions}",
            "Status": "✅ On Track" if accuracy >= 60 else "⚠️ Needs Focus"
        })
    
    return subject_summary

def calculate_chapter_stats(chapters_data):
    """Calculate statistics for chapters in selected subject"""
    chapter_stats = []
    chapters_list = list(chapters_data.keys())
    
    for chapter in chapters_list:
        attempts = chapters_data[chapter]
        avg_score = sum(s/t for s, t in attempts) / len(attempts) * 100
        latest_score, latest_total = attempts[0]
        latest_pct = (latest_score / latest_total) * 100
        best_score = max(s/t for s, t in attempts) * 100
        
        chapter_stats.append({
            "Chapter": chapter,
            "Average": avg_score,
            "Latest": latest_pct,
            "Best": best_score,
            "Attempts": len(attempts),
            "Status": "Strong" if avg_score >= 70 else "Needs Work" if avg_score < 50 else "Developing"
        })
    
    return chapter_stats, chapters_list

def create_progress_data(subject_data_raw, selected_subject):
    """Create progress data for overall trend"""
    progress_data = []
    for i, (subject, chapter, score, total) in enumerate(subject_data_raw):
        if subject == selected_subject:
            progress_data.append({
                "Attempt": len(progress_data) + 1,
                "Chapter": chapter,
                "Score": score,
                "Total": total,
                "Percentage": (score/total)*100
            })
    return progress_data