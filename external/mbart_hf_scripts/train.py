import argparse
import json
import torch
from transformers import MBartTokenizer, MBartForConditionalGeneration, TrainingArguments, Trainer

from dataset import MBartSummarizationDataset


def train(
    model_name,
    train_file,
    val_file,
    batch_size,
    output_dir,
    learning_rate,
    logging_steps,
    eval_steps,
    save_steps,
    warmup_steps,
    num_train_epochs,
    gradient_accumulation_steps,
    max_source_tokens_count,
    max_target_tokens_count
):
    tokenizer = MBartTokenizer.from_pretrained(model_name)
    train_dataset = MBartSummarizationDataset(
        train_file,
        tokenizer,
        max_source_tokens_count,
        max_target_tokens_count)
    val_dataset = MBartSummarizationDataset(
        val_file,
        tokenizer,
        max_source_tokens_count,
        max_target_tokens_count)
    model = MBartForConditionalGeneration.from_pretrained(model_name)
    training_args = TrainingArguments(
        output_dir=output_dir,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        do_train=True,
        do_eval=True,
        overwrite_output_dir=True,
        logging_steps=logging_steps,
        save_steps=save_steps,
        eval_steps=eval_steps,
        learning_rate=learning_rate,
        warmup_steps=warmup_steps,
        num_train_epochs=num_train_epochs,
        gradient_accumulation_steps=gradient_accumulation_steps,
        evaluation_strategy="steps"
    )
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset
    )
    trainer.train()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--train-file", type=str, required=True)
    parser.add_argument("--val-file", type=str, required=True)
    parser.add_argument("--model-name", type=str, default="facebook/mbart-large-cc25")
    parser.add_argument("--batch-size", type=int, default=2)
    parser.add_argument("--output-dir", type=str, required=True)
    parser.add_argument("--logging-steps", type=int, default=100)
    parser.add_argument("--save-steps", type=int, default=10000)
    parser.add_argument("--learning-rate", type=float, default=0.00003)
    parser.add_argument("--eval-steps", type=int, default=10000)
    parser.add_argument("--warmup-steps", type=int, default=1000)
    parser.add_argument("--num-train-epochs", type=int, default=2)
    parser.add_argument("--max-source-tokens-count", type=int, default=512)
    parser.add_argument("--max-target-tokens-count", type=int, default=128)
    parser.add_argument("--gradient-accumulation-steps", type=int, default=16)
    args = parser.parse_args()
    train(**vars(args))
