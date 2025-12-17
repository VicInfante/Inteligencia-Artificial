#!/usr/bin/env python3
import argparse
import os
import subprocess
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel


def main():
    parser = argparse.ArgumentParser(description="Convertir LoRA a GGUF para Ollama")
    parser.add_argument("--base", required=True, help="Ruta del modelo base (llama3)")
    parser.add_argument("--model", required=True, help="Ruta del LoRA entrenado")
    parser.add_argument("--out", required=True, help="Archivo GGUF de salida")
    parser.add_argument("--dtype", default="float16", choices=["float16", "float32"])
    args = parser.parse_args()

    print("🔹 Cargando tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(args.base)

    print("🔹 Cargando modelo base...")
    model = AutoModelForCausalLM.from_pretrained(
        args.base,
        torch_dtype=torch.float16 if args.dtype == "float16" else torch.float32,
        device_map="auto"
    )

    print("🔹 Cargando LoRA...")
    model = PeftModel.from_pretrained(model, args.model)

    print("🔹 Fusionando LoRA con el modelo base...")
    model = model.merge_and_unload()

    tmp_dir = "merged_model"
    os.makedirs(tmp_dir, exist_ok=True)

    print("🔹 Guardando modelo fusionado...")
    model.save_pretrained(tmp_dir, safe_serialization=True)
    tokenizer.save_pretrained(tmp_dir)

    print("🔹 Convirtiendo a GGUF...")
    llama_cpp_convert = "./llama.cpp/convert_hf_to_gguf.py"

    subprocess.run([
        "python",
        llama_cpp_convert,
        tmp_dir,
        "--outfile",
        args.out,
        "--outtype",
        "q8_0"
    ], check=True)

    print(f"✅ Conversión completa: {args.out}")


if __name__ == "__main__":
    main()