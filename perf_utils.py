# data_cleaner/perf_utils.py
import time
import psutil
import os
from contextlib import contextmanager
from typing import Optional, Dict, Any
from data_cleaner.logger_setup import setup_logging

logger = setup_logging()

class PerformanceTracker:
    """Track performance metrics across multiple operations."""
    
    def __init__(self):
        self.metrics: Dict[str, Dict[str, Any]] = {}
        self.start_time = time.perf_counter()
        self.start_memory = self._get_memory_mb()
    
    def _get_memory_mb(self) -> float:
        """Get current memory usage in MB."""
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / (1024 * 1024)
    
    def record_step(self, step_name: str, duration: float, memory_delta: float, memory_current: float):
        """Record metrics for a step."""
        self.metrics[step_name] = {
            'duration': duration,
            'memory_delta': memory_delta,
            'memory_current': memory_current,
            'timestamp': time.time()
        }
    
    def get_summary(self) -> Dict[str, Any]:
        """Get performance summary."""
        total_time = time.perf_counter() - self.start_time
        current_memory = self._get_memory_mb()
        total_memory_delta = current_memory - self.start_memory
        
        return {
            'total_time': total_time,
            'total_memory_delta': total_memory_delta,
            'current_memory': current_memory,
            'steps': self.metrics,
            'step_count': len(self.metrics)
        }
    
    def log_summary(self):
        """Log performance summary."""
        summary = self.get_summary()
        
        logger.info("=" * 60)
        logger.info("🎯 PERFORMANCE SUMMARY")
        logger.info("=" * 60)
        logger.info(f"⏱️  Total Runtime: {summary['total_time']:.2f}s")
        logger.info(f"💾 Memory Delta: {summary['total_memory_delta']:+.2f} MB")
        logger.info(f"🔄 Steps Completed: {summary['step_count']}")
        
        if summary['steps']:
            logger.info("\n📊 Step Details:")
            for step_name, metrics in summary['steps'].items():
                logger.info(
                    f"   • {step_name}: {metrics['duration']:.2f}s, "
                    f"Δ{metrics['memory_delta']:+.2f}MB"
                )
        logger.info("=" * 60)

# Global performance tracker instance
_global_tracker: Optional[PerformanceTracker] = None

def get_performance_tracker() -> PerformanceTracker:
    """Get or create global performance tracker."""
    global _global_tracker
    if _global_tracker is None:
        _global_tracker = PerformanceTracker()
    return _global_tracker

def reset_performance_tracker():
    """Reset the global performance tracker."""
    global _global_tracker
    _global_tracker = PerformanceTracker()

@contextmanager
def log_step(step_name: str, track_globally: bool = True):
    """
    Context manager for logging step performance with enhanced metrics.
    
    Args:
        step_name: Name of the step being executed
        track_globally: Whether to add metrics to global tracker
    """
    process = psutil.Process(os.getpid())
    mem_before = process.memory_info().rss / (1024 * 1024)
    start = time.perf_counter()
    
    # Log system info for the first step
    if step_name and not hasattr(log_step, '_first_run'):
        log_system_info()
        log_step._first_run = True
    
    logger.info(f"🚀 Starting step: {step_name}")
    
    try:
        yield
    except Exception as e:
        end = time.perf_counter()
        mem_after = process.memory_info().rss / (1024 * 1024)
        logger.error(
            f"❌ Failed step: {step_name} | "
            f"Time: {end - start:.2f}s | Memory: {mem_after:.2f} MB | "
            f"Error: {str(e)}"
        )
        raise
    finally:
        end = time.perf_counter()
        mem_after = process.memory_info().rss / (1024 * 1024)
        mem_delta = mem_after - mem_before
        duration = end - start
        
        # Choose appropriate emoji based on performance
        if duration < 1:
            time_emoji = "⚡"  # Fast
        elif duration < 10:
            time_emoji = "✅"  # Normal
        else:
            time_emoji = "🐌"  # Slow
        
        memory_emoji = "📈" if mem_delta > 0 else "📉" if mem_delta < 0 else "📊"
        
        logger.info(
            f"{time_emoji} Finished step: {step_name} | "
            f"Time: {duration:.2f}s | "
            f"{memory_emoji} Memory Δ: {mem_delta:+.2f} MB (now {mem_after:.2f} MB)"
        )
        
        # Track globally if requested
        if track_globally:
            tracker = get_performance_tracker()
            tracker.record_step(step_name, duration, mem_delta, mem_after)

def log_system_info():
    """Log system information for debugging and optimization."""
    try:
        # CPU information
        cpu_count = psutil.cpu_count()
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # Memory information
        memory = psutil.virtual_memory()
        memory_total_gb = memory.total / (1024**3)
        memory_available_gb = memory.available / (1024**3)
        memory_percent = memory.percent
        
        # Disk information for current directory
        disk = psutil.disk_usage('.')
        disk_free_gb = disk.free / (1024**3)
        
        logger.info("🖥️  SYSTEM INFORMATION")
        logger.info(f"   CPU: {cpu_count} cores, {cpu_percent:.1f}% used")
        logger.info(f"   Memory: {memory_available_gb:.1f}GB available / {memory_total_gb:.1f}GB total ({memory_percent:.1f}% used)")
        logger.info(f"   Disk: {disk_free_gb:.1f}GB free space")
        
    except Exception as e:
        logger.warning(f"⚠️ Could not gather system info: {e}")

def check_system_resources(file_path: str, max_memory_gb: float = 8.0) -> Dict[str, Any]:
    """
    Check if system has enough resources to process file.
    
    Args:
        file_path: Path to file to be processed
        max_memory_gb: Maximum recommended file size in GB
        
    Returns:
        Dict with resource information and recommendations
    """
    try:
        file_size_bytes = os.path.getsize(file_path)
        file_size_gb = file_size_bytes / (1024**3)
        
        memory = psutil.virtual_memory()
        available_memory_gb = memory.available / (1024**3)
        
        # Calculate recommendations
        recommended_chunk_size = 100_000  # Default
        use_streaming = False
        
        if file_size_gb > max_memory_gb:
            logger.warning(f"⚠️ Large file detected: {file_size_gb:.2f}GB")
            use_streaming = True
            recommended_chunk_size = 50_000
        
        if available_memory_gb < (file_size_gb * 2):
            logger.warning(
                f"⚠️ Low memory: {available_memory_gb:.2f}GB available for {file_size_gb:.2f}GB file"
            )
            use_streaming = True
            recommended_chunk_size = min(recommended_chunk_size, 25_000)
        
        return {
            'file_size_gb': file_size_gb,
            'available_memory_gb': available_memory_gb,
            'recommended_chunk_size': recommended_chunk_size,
            'use_streaming': use_streaming,
            'memory_ratio': file_size_gb / available_memory_gb if available_memory_gb > 0 else float('inf')
        }
        
    except Exception as e:
        logger.error(f"❌ Error checking system resources: {e}")
        return {
            'file_size_gb': 0,
            'available_memory_gb': 0,
            'recommended_chunk_size': 100_000,
            'use_streaming': False,
            'memory_ratio': 0,
            'error': str(e)
        }

@contextmanager
def memory_monitor(warning_threshold_mb: float = 1000):
    """
    Monitor memory usage and warn if it exceeds threshold.
    
    Args:
        warning_threshold_mb: Memory usage threshold in MB to trigger warning
    """
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss / (1024 * 1024)
    
    try:
        yield
    finally:
        final_memory = process.memory_info().rss / (1024 * 1024)
        memory_increase = final_memory - initial_memory
        
        if memory_increase > warning_threshold_mb:
            logger.warning(
                f"⚠️ High memory usage detected: +{memory_increase:.2f}MB "
                f"(now using {final_memory:.2f}MB)"
            )

def format_duration(seconds: float) -> str:
    """Format duration in human readable format."""
    if seconds < 1:
        return f"{seconds*1000:.0f}ms"
    elif seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes}m {secs:.0f}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"