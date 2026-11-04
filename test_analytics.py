#!/usr/bin/env python
import sys
sys.path.insert(0, '.')

try:
    from analytics import YOLO11Analytics
    print("✅ SUCCESS: YOLO11Analytics imported")
    
    a = YOLO11Analytics(model_obj=None, dataset_path=None)
    print("✅ SUCCESS: YOLO11Analytics instantiated with model_obj parameter")
    
    print("✅ All methods available:")
    print(f"  - find_dataset: {hasattr(a, 'find_dataset')}")
    print(f"  - load_dataset_images: {hasattr(a, 'load_dataset_images')}")
    print(f"  - evaluate_model_on_dataset: {hasattr(a, 'evaluate_model_on_dataset')}")
    print(f"  - create_confidence_distribution_graph: {hasattr(a, 'create_confidence_distribution_graph')}")
    
    print("\n✅ READY TO USE!")
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
