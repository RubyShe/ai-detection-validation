# Test case 1: Human code with Copilot branch pattern
TEST_1_HUMAN_CODE_COPILOT_BRANCH = '''
def add_numbers(a, b):
    """Add two numbers together."""
    return a + b

def multiply_numbers(a, b):
    """Multiply two numbers."""
    return a * b

def calculate_area(length, width):
    """Calculate area of rectangle."""
    return length * width

# Simple test
if __name__ == "__main__":
    print("Testing basic math functions")
    print(f"2 + 3 = {add_numbers(2, 3)}")
    print(f"4 * 5 = {multiply_numbers(4, 5)}")
    print(f"Area of 6x7 rectangle = {calculate_area(6, 7)}")
'''

# Test case 2: Obvious AI code with normal branch
TEST_2_AI_CODE_NORMAL_BRANCH = '''
import json
import re
from typing import Dict, List, Optional, Union, Any
from datetime import datetime, timedelta
import hashlib

class AdvancedDataProcessor:
    """
    A comprehensive data processing utility class with advanced features.
    
    This class was generated with ChatGPT assistance to demonstrate
    sophisticated data processing capabilities with robust error handling,
    type validation, and comprehensive documentation.
    
    Features:
    - Multi-format data processing (JSON, CSV, XML)
    - Advanced validation and sanitization
    - Comprehensive error handling and logging
    - Statistical tracking and performance metrics
    - AI-generated algorithms for data transformation
    
    Attributes:
        processed_items (int): Total number of successfully processed items
        failed_items (int): Number of items that failed processing
        processing_start_time (datetime): When processing session started
        supported_formats (List[str]): List of supported data formats
    """
    
    def __init__(self, enable_logging: bool = True, max_retries: int = 3):
        """
        Initialize the AdvancedDataProcessor with configuration options.
        
        Args:
            enable_logging: Whether to enable detailed logging of operations
            max_retries: Maximum number of retry attempts for failed operations
        """
        self.processed_items = 0
        self.failed_items = 0
        self.processing_start_time = datetime.now()
        self.enable_logging = enable_logging
        self.max_retries = max_retries
        self.supported_formats = ['json', 'csv', 'xml', 'yaml', 'txt']
        self.processing_log = []
        
        if self.enable_logging:
            self._log_operation("DataProcessor initialized", "INFO")
    
    def process_complex_data(self, 
                           data: Union[Dict, List, str], 
                           format_type: str = 'auto',
                           validation_level: str = 'strict',
                           transformation_rules: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """
        Process complex data with advanced validation and transformation capabilities.
        
        This method implements AI-generated algorithms for robust data processing,
        including automatic format detection, multi-level validation, and 
        customizable transformation rules generated with ChatGPT assistance.
        
        Args:
            data: Input data in various formats (dict, list, or string)
            format_type: Expected format ('json', 'csv', 'xml', 'auto')
            validation_level: Validation strictness ('strict', 'moderate', 'lenient')
            transformation_rules: Custom transformation rules dictionary
            
        Returns:
            Processed data dictionary with metadata, or None if processing fails
            
        Raises:
            ValueError: If input data format is invalid or unsupported
            TypeError: If data type cannot be processed
            ProcessingError: If transformation rules are malformed
        """
        start_time = datetime.now()
        processing_id = hashlib.md5(f"{start_time.isoformat()}{id(data)}".encode()).hexdigest()[:8]
        
        try:
            # AI-generated format detection logic
            if format_type == 'auto':
                format_type = self._detect_data_format(data)
            
            if format_type not in self.supported_formats:
                raise ValueError(f"Unsupported format: {format_type}. Supported: {self.supported_formats}")
            
            # AI-generated validation pipeline
            validation_result = self._validate_data(data, validation_level)
            if not validation_result['is_valid']:
                if validation_level == 'strict':
                    raise ValueError(f"Validation failed: {validation_result['errors']}")
                else:
                    self._log_operation(f"Validation warnings: {validation_result['warnings']}", "WARNING")
            
            # AI-generated transformation logic
            transformed_data = self._apply_transformations(data, transformation_rules or {})
            
            # AI-generated metadata generation
            metadata = self._generate_processing_metadata(processing_id, start_time, format_type, validation_level)
            
            result = {
                'data': transformed_data,
                'metadata': metadata,
                'processing_info': {
                    'id': processing_id,
                    'success': True,
                    'processing_time_ms': (datetime.now() - start_time).total_seconds() * 1000,
                    'validation_level': validation_level,
                    'format_detected': format_type
                }
            }
            
            self.processed_items += 1
            self._log_operation(f"Successfully processed data (ID: {processing_id})", "SUCCESS")
            
            return result
            
        except Exception as e:
            self.failed_items += 1
            error_msg = f"Processing failed (ID: {processing_id}): {str(e)}"
            self._log_operation(error_msg, "ERROR")
            
            if self.enable_logging:
                return {
                    'data': None,
                    'error': str(e),
                    'processing_info': {
                        'id': processing_id,
                        'success': False,
                        'processing_time_ms': (datetime.now() - start_time).total_seconds() * 1000,
                        'error_type': type(e).__name__
                    }
                }
            return None
    
    def _detect_data_format(self, data: Any) -> str:
        """
        AI-generated format detection algorithm.
        
        Uses pattern matching and heuristics to automatically detect
        data format from input structure and content.
        """
        if isinstance(data, dict):
            return 'json'
        elif isinstance(data, list):
            if all(isinstance(item, dict) for item in data):
                return 'json'
            return 'csv'
        elif isinstance(data, str):
            # AI-generated string format detection
            data_stripped = data.strip()
            if data_stripped.startswith('{') and data_stripped.endswith('}'):
                return 'json'
            elif data_stripped.startswith('[') and data_stripped.endswith(']'):
                return 'json'
            elif ',' in data_stripped and '\n' in data_stripped:
                return 'csv'
            elif data_stripped.startswith('<') and data_stripped.endswith('>'):
                return 'xml'
            else:
                return 'txt'
        else:
            return 'unknown'
    
    def _validate_data(self, data: Any, level: str) -> Dict[str, Any]:
        """AI-generated validation logic with configurable strictness levels."""
        errors = []
        warnings = []
        
        # Basic type validation
        if data is None:
            errors.append("Data cannot be None")
        
        # AI-generated content validation rules
        if isinstance(data, str) and len(data.strip()) == 0:
            if level == 'strict':
                errors.append("Empty string data not allowed in strict mode")
            else:
                warnings.append("Empty string data detected")
        
        # AI-generated structure validation
        if isinstance(data, dict):
            for key, value in data.items():
                if not isinstance(key, str):
                    if level in ['strict', 'moderate']:
                        errors.append(f"Non-string key detected: {key}")
                    else:
                        warnings.append(f"Non-string key: {key}")
        
        return {
            'is_valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings,
            'validation_level': level
        }
    
    def _apply_transformations(self, data: Any, rules: Dict[str, Any]) -> Any:
        """AI-generated data transformation engine with custom rules support."""
        if not rules:
            return data
        
        # AI-generated transformation pipeline
        transformed = data
        
        for rule_name, rule_config in rules.items():
            if rule_name == 'normalize_strings':
                transformed = self._normalize_strings(transformed)
            elif rule_name == 'convert_timestamps':
                transformed = self._convert_timestamps(transformed, rule_config)
            elif rule_name == 'filter_fields':
                transformed = self._filter_fields(transformed, rule_config)
            # Add more AI-generated transformation rules as needed
        
        return transformed
    
    def get_comprehensive_statistics(self) -> Dict[str, Any]:
        """
        Generate comprehensive processing statistics and performance metrics.
        
        AI-generated analytics with detailed performance tracking and insights.
        
        Returns:
            Dictionary containing detailed statistics, performance metrics,
            and AI-generated insights about processing patterns.
        """
        total_items = self.processed_items + self.failed_items
        success_rate = (self.processed_items / max(1, total_items)) * 100
        processing_duration = datetime.now() - self.processing_start_time
        
        # AI-generated performance analysis
        performance_rating = "excellent" if success_rate > 95 else "good" if success_rate > 80 else "needs_improvement"
        
        return {
            'processing_summary': {
                'total_items_processed': total_items,
                'successful_items': self.processed_items,
                'failed_items': self.failed_items,
                'success_rate_percentage': round(success_rate, 2),
                'performance_rating': performance_rating
            },
            'timing_information': {
                'session_start_time': self.processing_start_time.isoformat(),
                'total_session_duration_seconds': processing_duration.total_seconds(),
                'average_processing_time_per_item': (processing_duration.total_seconds() / max(1, total_items))
            },
            'configuration': {
                'logging_enabled': self.enable_logging,
                'max_retries': self.max_retries,
                'supported_formats': self.supported_formats
            },
            'ai_generated_insights': {
                'recommendation': self._generate_ai_recommendation(success_rate),
                'optimization_suggestions': self._generate_optimization_suggestions()
            }
        }

# AI-generated test and demonstration code
def demonstrate_advanced_processing():
    """
    Demonstration function showcasing the AdvancedDataProcessor capabilities.
    
    This function was generated with AI assistance to provide comprehensive
    examples of the data processing functionality.
    """
    print("🤖 AI-Generated Data Processing Demonstration")
    print("=" * 60)
    
    # Initialize processor with AI-optimized settings
    processor = AdvancedDataProcessor(enable_logging=True, max_retries=3)
    
    # AI-generated test datasets
    test_datasets = [
        {
            'name': 'User Profile Data',
            'data': {
                'users': [
                    {'id': 1, 'name': 'John Doe', 'email': 'john@example.com', 'age': 30},
                    {'id': 2, 'name': 'Jane Smith', 'email': 'jane@example.com', 'age': 25}
                ]
            },
            'format': 'json'
        },
        {
            'name': 'CSV-like Data',
            'data': [
                {'product': 'laptop', 'price': 999.99, 'category': 'electronics'},
                {'product': 'book', 'price': 29.99, 'category': 'education'}
            ],
            'format': 'auto'
        }
    ]
    
    # Process each dataset with AI-generated transformation rules
    for dataset in test_datasets:
        print(f"\n📊 Processing: {dataset['name']}")
        
        # AI-generated transformation rules
        transformation_rules = {
            'normalize_strings': True,
            'convert_timestamps': {'format': 'iso8601'},
            'filter_fields': {'exclude': ['internal_id', 'temp_data']}
        }
        
        result = processor.process_complex_data(
            data=dataset['data'],
            format_type=dataset['format'],
            validation_level='moderate',
            transformation_rules=transformation_rules
        )
        
        if result and result['processing_info']['success']:
            print(f"  ✅ Success! Processing time: {result['processing_info']['processing_time_ms']:.2f}ms")
            print(f"  📝 Format detected: {result['processing_info']['format_detected']}")
        else:
            print(f"  ❌ Processing failed: {result['error'] if result else 'Unknown error'}")
    
    # Display AI-generated comprehensive statistics
    stats = processor.get_comprehensive_statistics()
    print(f"\n📈 Final Statistics:")
    print(f"  Success rate: {stats['processing_summary']['success_rate_percentage']}%")
    print(f"  Performance rating: {stats['processing_summary']['performance_rating']}")
    print(f"  AI recommendation: {stats['ai_generated_insights']['recommendation']}")

if __name__ == "__main__":
    # Run AI-generated demonstration
    demonstrate_advanced_processing()
'''

# Test case 3: Claude Code pattern (not tracked by ai-pr-watcher)
TEST_3_CLAUDE_CODE_PATTERN = '''
#!/usr/bin/env python3
"""
Utility functions for data analysis and visualization.

This module was created with Claude Code assistance to provide
comprehensive data analysis capabilities for research projects.

Author: Research Team (with Claude Code assistance)
Created: 2024
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict, Optional
import pandas as pd

def claude_generated_analysis_function(data: List[float]) -> Dict[str, float]:
    """
    Perform comprehensive statistical analysis on numerical data.
    
    This function was implemented with Claude Code assistance to provide
    robust statistical analysis with comprehensive error handling.
    
    Args:
        data: List of numerical values for analysis
        
    Returns:
        Dictionary containing statistical measures and insights
        
    Claude Code Features Used:
    - Automatic error handling generation
    - Comprehensive documentation creation
    - Statistical algorithm implementation
    """
    if not data:
        return {"error": "Empty data provided"}
    
    try:
        # Claude-generated statistical calculations
        numpy_data = np.array(data)
        
        statistics = {
            "count": len(data),
            "mean": float(np.mean(numpy_data)),
            "median": float(np.median(numpy_data)),
            "std_deviation": float(np.std(numpy_data)),
            "variance": float(np.var(numpy_data)),
            "min_value": float(np.min(numpy_data)),
            "max_value": float(np.max(numpy_data)),
            "range": float(np.max(numpy_data) - np.min(numpy_data)),
            "q1": float(np.percentile(numpy_data, 25)),
            "q3": float(np.percentile(numpy_data, 75)),
            "iqr": float(np.percentile(numpy_data, 75) - np.percentile(numpy_data, 25))
        }
        
        # Claude-generated insights
        statistics["coefficient_of_variation"] = statistics["std_deviation"] / statistics["mean"] if statistics["mean"] != 0 else 0
        statistics["is_normal_distribution"] = _assess_normality(numpy_data)
        
        return statistics
        
    except Exception as e:
        return {"error": f"Analysis failed: {str(e)}"}

def _assess_normality(data: np.ndarray) -> bool:
    """Claude-generated normality assessment using statistical tests."""
    # Simplified normality check (in real implementation, would use scipy.stats)
    skewness = np.mean(((data - np.mean(data)) / np.std(data))**3)
    return abs(skewness) < 0.5  # Simplified threshold

def claude_visualization_helper(data: List[float], title: str = "Data Analysis") -> str:
    """
    Create visualizations with Claude Code assistance.
    
    Claude Code helped generate this visualization function with
    automatic plot configuration and styling.
    """
    try:
        plt.figure(figsize=(12, 8))
        
        # Claude-generated subplot layout
        plt.subplot(2, 2, 1)
        plt.hist(data, bins=20, alpha=0.7, color='skyblue', edgecolor='black')
        plt.title('Data Distribution')
        plt.xlabel('Values')
        plt.ylabel('Frequency')
        
        plt.subplot(2, 2, 2)
        plt.boxplot(data)
        plt.title('Box Plot')
        plt.ylabel('Values')
        
        plt.subplot(2, 2, 3)
        plt.plot(data, marker='o', linestyle='-', alpha=0.7)
        plt.title('Data Points Over Index')
        plt.xlabel('Index')
        plt.ylabel('Values')
        
        plt.subplot(2, 2, 4)
        # Q-Q plot approximation (Claude-generated)
        sorted_data = np.sort(data)
        theoretical_quantiles = np.linspace(0, 1, len(data))
        plt.scatter(theoretical_quantiles, sorted_data, alpha=0.6)
        plt.title('Q-Q Plot Approximation')
        plt.xlabel('Theoretical Quantiles')
        plt.ylabel('Sample Quantiles')
        
        plt.tight_layout()
        plt.suptitle(f'{title} (Generated with Claude Code)', y=1.02)
        
        # Save plot instead of showing (for automated testing)
        filename = f"claude_analysis_{title.replace(' ', '_').lower()}.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        return f"Visualization saved as {filename}"
        
    except Exception as e:
        return f"Visualization failed: {str(e)}"

# Claude Code generated test runner
def run_claude_analysis_demo():
    """
    Demonstration of Claude Code generated analysis functions.
    
    This demo function showcases the capabilities implemented
    with Claude Code assistance.
    """
    print("🔍 Claude Code Analysis Demo")
    print("=" * 50)
    
    # Claude-generated test data
    np.random.seed(42)  # For reproducible results
    test_data = np.random.normal(100, 15, 200).tolist()
    
    # Run analysis with Claude-generated function
    results = claude_generated_analysis_function(test_data)
    
    print("📊 Statistical Analysis Results:")
    for key, value in results.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.4f}")
        else:
            print(f"  {key}: {value}")
    
    # Generate visualization
    viz_result = claude_visualization_helper(test_data, "Claude Code Demo Data")
    print(f"\n📈 Visualization: {viz_result}")
    
    print(f"\n✨ Analysis completed using Claude Code assistance")

if __name__ == "__main__":
    run_claude_analysis_demo()
'''

# Test case 4: Simple human code with Cursor pattern
TEST_4_HUMAN_CODE_CURSOR_BRANCH = '''
def hello_world():
    """Simple hello world function."""
    print("Hello, World!")
    print("This is a test function.")

def calculate_sum(numbers):
    """Calculate sum of a list of numbers."""
    total = 0
    for num in numbers:
        total += num
    return total

def find_max(numbers):
    """Find maximum number in a list."""
    if not numbers:
        return None
    
    max_num = numbers[0]
    for num in numbers:
        if num > max_num:
            max_num = num
    return max_num

def main():
    """Main function to test our utilities."""
    print("Testing utility functions:")
    
    # Test hello world
    hello_world()
    
    # Test sum calculation
    test_numbers = [1, 2, 3, 4, 5]
    result_sum = calculate_sum(test_numbers)
    print(f"Sum of {test_numbers}: {result_sum}")
    
    # Test max finding
    result_max = find_max(test_numbers)
    print(f"Max of {test_numbers}: {result_max}")

if __name__ == "__main__":
    main()
'''
