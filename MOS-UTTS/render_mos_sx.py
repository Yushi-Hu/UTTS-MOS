#!/usr/bin/env python3
"""Generate forms for human evaluation."""

import os
import random
from jinja2 import FileSystemLoader, Environment

random.seed(1234)


def main():
    """Main function."""
    loader = FileSystemLoader(searchpath="./templates")
    env = Environment(loader=loader)
    template = env.get_template("mos.html_wo_text.jinja2")

    wav_base_dir = 'wavs'
    models = os.listdir(wav_base_dir)
    wav_fids = os.listdir(f'{wav_base_dir}/{models[0]}')
    wav_fids.sort()

    part_name = "part1" # all/part1/part2

    num_samples = 1 #len(wav_fids) // 2

    if part_name == "all":
        form_id = 1
    elif part_name == "part1":
        wav_fids = wav_fids[:num_samples]
        form_id = 2
    else:
        wav_fids = wav_fids[num_samples:]
        form_id = 3

    wav_paths = []
    for fid in wav_fids:
        cur_group = []
        random.shuffle(models)
        for m in models:
            cur_group.append(f"{wav_base_dir}/{m}/{fid}")
        wav_paths.append(cur_group)

    if part_name == "all":
        with open('fid_orders_all.txt', 'w') as f:
            for groups in wav_paths:
                f.write('\n'.join(groups) + '\n')
    elif part_name == "part1":
        with open('fid_orders_part1.txt', 'w') as f:
            for groups in wav_paths:
                f.write('\n'.join(groups) + '\n')
    else:
        with open('fid_orders_part2.txt', 'w') as f:
            for groups in wav_paths:
                f.write('\n'.join(groups) + '\n')

    questions = []
    cnt = 1
    for i, group in enumerate(wav_paths):
        for j, sample in enumerate(group):
            questions.append(
                {
                    "title": f"Audio{i}-model{j}",
                    "audio_path": sample,
                    "name": f"q{cnt}"
                }
            )
            cnt += 1

    html = template.render(
        page_title=f"MOS Test {form_id}",
        form_url="https://script.google.com/macros/s/AKfycbwp_Jem-MF9hgOZv9pAhxQrzXsBI3IP4EjeRLMkcE0fLJYUkv19iuPRgWdiN3AYfzwC7Q/exec",
        form_id=form_id,
        questions=questions,
    )
    print(html)


if __name__ == "__main__":
    main()
