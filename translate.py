from transformers import MBartForConditionalGeneration, MBart50TokenizerFast

def translator(input_text, src_lang, tgt_lang):
    
    model = MBartForConditionalGeneration.from_pretrained('facebook/mbart-large-50-many-to-many-mmt')
    tokenizer = MBart50TokenizerFast.from_pretrained('facebook/mbart-large-50-many-to-many-mmt')
    supported_langs = ['en_XX', 'gu_IN', 'hi_IN', 'bn_IN', 'ml_IN', 'mr_IN', 'ta_IN', 'te_IN']

    if src_lang not in supported_langs:
        raise RuntimeError('Unsupported source language.')
    if tgt_lang not in supported_langs:
        raise RuntimeError('Unsupported target language.')

    tokenizer.src_lang = src_lang
    encoded_text = tokenizer(input_text, return_tensors='pt')
    generated_tokens = model.generate(
        **encoded_text, forced_bos_token_id=tokenizer.lang_code_to_id[tgt_lang])
    output_text_arr = tokenizer.batch_decode(
        generated_tokens, skip_special_tokens=True)

    if len(output_text_arr) > 0:
        return output_text_arr[0]
    else:
        raise RuntimeError(
            'Failed to generate output. Output Text Array is empty.')
