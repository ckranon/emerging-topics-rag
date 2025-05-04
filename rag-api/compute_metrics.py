#!/usr/bin/env python3
"""
Standalone test script to evaluate a saved RAG dataset using various metrics.

Usage:
  python3 test_evaluate.py --dataset path/to/eval_dataset_with_gt \
                           [--workers 8] [--timeout 120]
"""
import argparse
from datasets import load_from_disk
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    answer_correctness,
    context_precision,
    #ContextUtilization,
    context_recall,
    answer_similarity,
)
from ragas.run_config import RunConfig
import sys


def parse_args():
    parser = argparse.ArgumentParser(
        description="Evaluate a RAG-generated dataset with multiple metrics."
    )
    parser.add_argument(
        "--dataset",
        type=str,
        default="eval_dataset_with_gt",
        help="Path to the Hugging Face dataset directory with user_input, response, retrieved_contexts, and references columns",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=8,
        help="Maximum number of parallel workers",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=120,
        help="Timeout (in seconds) for each evaluation task",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Load the dataset
    print(f"Loading dataset from '{args.dataset}'...")
    dataset = load_from_disk(args.dataset)
    print(f"Dataset contains {len(dataset)} records.")

    # Define evaluation metrics
    metrics = [
        faithfulness,
        answer_relevancy,
        answer_correctness,
        context_precision,
        #ContextUtilization,
        context_recall,
        answer_similarity,
    ]

    # Configure evaluation
    run_cfg = RunConfig(max_workers=args.workers, timeout=args.timeout)
    print("Running evaluation with metrics:")
    for m in metrics:
        print(f"  - {m.name}")

    # Execute evaluation
    results = evaluate(
        dataset,
        metrics,
        run_config=run_cfg,
        raise_exceptions=False
    )

    # Output results
    print("\n=== Evaluation Results ===")
    for metric_name, score in results.items():
        print(f"{metric_name}: {score:.2f}")


if __name__ == "__main__":
    main()
