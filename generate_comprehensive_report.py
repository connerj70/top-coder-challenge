#!/usr/bin/env python3
"""
Generate Comprehensive Error Analysis Report

This script creates a complete error analysis report that combines all our 
error analysis frameworks and provides actionable insights for improving 
the reimbursement calculation model.
"""

from calculate_reimbursement import *
from datetime import datetime

def main():
    """Generate the comprehensive error analysis report."""
    print("🔍 COMPREHENSIVE ERROR ANALYSIS REPORT GENERATOR")
    print("="*60)
    print()
    
    # Load test cases
    print("📋 Loading test cases...")
    test_cases = load_public_test_cases('public_cases.json')
    total_cases = len(test_cases)
    print(f"   Loaded {total_cases} test cases")
    
    # Determine sample size
    sample_size = min(100, total_cases)  # Use up to 100 cases for comprehensive analysis
    print(f"   Analyzing first {sample_size} cases for detailed insights")
    print()
    
    # Generate timestamp for report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"error_analysis_report_{timestamp}.md"
    
    print(f"📊 Generating comprehensive error analysis report...")
    print(f"   Report will be saved as: {report_filename}")
    print()
    
    # Generate the comprehensive report
    try:
        report_result = generate_comprehensive_error_report(
            test_cases, 
            sample_size=sample_size, 
            output_file=report_filename
        )
        
        # Extract key insights for console summary
        structured_report = report_result['structured_report']
        
        print("\n" + "="*60)
        print("REPORT GENERATION COMPLETE")
        print("="*60)
        
        # Display key metrics
        exec_summary = structured_report['executive_summary']
        performance = structured_report['model_performance_summary']
        
        print(f"\n📈 EXECUTIVE SUMMARY:")
        print(f"   Model Status: {exec_summary['model_status']}")
        print(f"   Performance Grade: {performance['performance_grade']}")
        print(f"   Overall Accuracy (5%): {exec_summary['overall_accuracy']:.1f}%")
        print(f"   Cases Analyzed: {exec_summary['total_cases_analyzed']}")
        
        print(f"\n🚨 CRITICAL ISSUES IDENTIFIED:")
        for i, issue in enumerate(exec_summary['critical_issues'], 1):
            print(f"   {i}. {issue}")
        
        print(f"\n🎯 IMMEDIATE ACTION ITEMS:")
        immediate_actions = structured_report['actionable_recommendations']['immediate_actions']
        for action in immediate_actions:
            print(f"   Priority {action['priority']}: {action['action']}")
            print(f"      Target: {action['target']}")
            print(f"      Impact: {action['expected_impact']}")
            print()
        
        print(f"📄 FULL REPORT SAVED TO: {report_filename}")
        print(f"📊 STRUCTURED DATA AVAILABLE in script return value")
        
        # Save structured report as JSON for programmatic access
        json_filename = f"error_analysis_data_{timestamp}.json"
        try:
            import json
            with open(json_filename, 'w') as f:
                # Convert to JSON-serializable format
                json_data = convert_to_json_serializable(structured_report)
                json.dump(json_data, f, indent=2)
            print(f"📊 STRUCTURED DATA SAVED TO: {json_filename}")
        except Exception as e:
            print(f"⚠️  Could not save JSON data: {e}")
        
        print("\n" + "="*60)
        print("NEXT STEPS:")
        print("="*60)
        print("1. Review the comprehensive report for detailed analysis")
        print("2. Prioritize immediate fixes based on severity and impact")
        print("3. Implement Phase 1 critical fixes (1-2 weeks)")
        print("4. Monitor improvement with follow-up error analysis")
        print("5. Proceed to Phase 2 accuracy improvements")
        print()
        
        return report_result
        
    except Exception as e:
        print(f"❌ Error generating report: {e}")
        import traceback
        traceback.print_exc()
        return None

def convert_to_json_serializable(obj):
    """Convert complex objects to JSON-serializable format."""
    if isinstance(obj, dict):
        return {key: convert_to_json_serializable(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_json_serializable(item) for item in obj]
    elif hasattr(obj, '__dict__'):
        return convert_to_json_serializable(obj.__dict__)
    else:
        return obj

if __name__ == "__main__":
    # Run the comprehensive report generation
    report_result = main()
    
    # If running interactively, provide access to the structured report
    if report_result:
        print(f"\n🔧 For programmatic access:")
        print(f"   structured_report = report_result['structured_report']")
        print(f"   narrative_report = report_result['narrative_report']")
        print()
        print(f"🚀 Ready to proceed with Task 8: Refine calculation logic based on error analysis!") 