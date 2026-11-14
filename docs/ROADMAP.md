# MiniLLM roadmap

The goal is to finish a small model that can learn from short stories and generate text, and understand it well enough to explain and recreate the work. Each phase should leave us with something working that we can inspect and demonstrate.

This is the current working plan from our project chat. We can revise it as we learn. The [original proposal](project-proposal-original.docx) records the initial ambition; it is preserved unchanged. The working plan prioritizes a complete local project before conversational training or larger models. Any formal proposal revision should be saved separately from the original.

## Phase 0: Set up the project

Create the Git repository, give the project its own Python environment, install PyTorch, and verify that the Mac GPU can perform calculations and compute derivatives. Derivatives tell us how an output changes when its inputs change; training uses them to work out how to adjust the model.

Complete when the environment works, the setup can be recreated from the documentation, and the setup files are saved in a Git commit.

Status: complete. The original environment and GPU checks passed, and Adam successfully recreated a separate environment from requirements.txt and repeated the dependency and GPU checks. Package versions are recorded, the environment folder is ignored by Git, and [setup instructions](SETUP.md) are written. The setup files were saved in commit `b03a3ef`, verified in the local Git history on November 13, 2026.

## Phase 1: Prepare stories for the model

Start with a small portion of TinyStories. Build a tokenizer, which converts text into numbered pieces called tokens and converts them back into text. Arrange the tokens into small groups of examples: the model sees some tokens and tries to predict the following ones. Keep training examples separate from validation examples, which we use to check learning on stories the model has not trained on.

Complete when text can be converted to tokens and back, and we can inspect correctly paired inputs and next-token targets.

Progress: Adam implemented and verified character encoding, decoding, and input/target sequences shifted by one character using a small text example. He correctly identified the space as the next-token target after `cat` and explained why rebuilding the vocabulary includes a newly added character. `tokenizer.py` now contains only reusable `encode(raw_text, char_to_id)` and `decode(encoded_text, characters)` functions, with the vocabulary supplied explicitly. An assistant check verified that importing the module produces no demo output, the toy text round trip passes, and an unsupported character raises `KeyError`. Adam connected the functions to the training vocabulary in `inspect_data.py`; his run verified an exact first-story round trip with 701 characters and 701 tokens. He extended the checks to both sampled splits; an assistant run verified that all 1,000 training and 100 validation stories pass exact round trips with the same training vocabulary.

Adam identified improving training performance alongside worsening validation performance as overfitting. Datasets 5.2.0 is installed in the project environment; its import and `pip check` passed, and the installed versions are recorded in requirements.txt. `inspect_data.py` successfully streamed and printed three TinyStories training examples, verified by both an assistant run and Adam's terminal output. It also collected their distinct characters, with both runs confirming a vocabulary size of 49. The unauthenticated-request warning did not prevent loading.

The inspected sample now contains the first 1,000 training stories: 941,640 characters and 75 distinct characters, verified by Adam's output and an assistant run. Some source passages contain garbled sequences such as `â€™`; no cleaning has been applied. Available dataset splits were verified as `train` and `validation`. Adam's run of the updated inspection script loaded 100 validation stories and reported no characters outside the unchanged training vocabulary; the saved code was checked. These sample sizes remain provisional.

## Phase 2: Build and understand the model

Implement a tiny decoder-only Transformer in PyTorch. This is a model that predicts the next token using earlier tokens. Learn each part before implementing it, including how tokens become vectors of numbers and how attention lets the model use earlier context. Start around one million adjustable values, called parameters; exact dimensions remain provisional.

Complete when the model computes predictions and gradients, and can learn one small batch extremely well. This small memorization test helps expose implementation problems before longer training.

## Phase 3: Train on stories

Teach the model using more examples. Record training and validation loss, numerical measures of prediction error, so we can see whether it is improving. Save checkpoints, which let us reload the model and resume training, and generate text from the same starting prompts at several points.

Complete when a saved model can be reloaded and used to generate text, with recorded losses, training time, and sample outputs.

## Phase 4: Finish the presentation baseline

Make the story-generation demo easy to run. Assemble the learning curves, example outputs, model size, training time, and an honest explanation of what works and what is limited.

Complete when someone can follow the setup instructions, run the demo, and understand what was built and learned. This is a complete project even if we stop here.

## Phase 5: Explore conversations (optional)

Fine-tune the pretrained model, meaning train it further on conversational examples, and compare its responses before and after. Add a simple interaction interface if useful. Discuss the likely limits of a tiny story-trained model before committing to this phase.

Complete when we can demonstrate and evaluate what conversational training changed, including its limitations.

## Phase 6: Explore extensions (optional)

Possible experiments include a 20–30 million parameter model, rented GPUs, a subset of FineWeb-Edu, and KV caching, which reuses earlier attention calculations during generation. Choose extensions based on what we want to learn, available time, and an agreed compute budget.

Complete each chosen experiment with a working result and a comparison against the smaller baseline. These experiments are not required for project completion.

## Where to resume

Adam constructed a real-story next-token window and reported inputs `One day,`, targets `ne day, `, and lengths of eight each; the saved slicing code was checked. Continue Phase 1 by grouping four such windows into input and target PyTorch tensors and inspecting their shapes and first row. The window and batch sizes are illustrations, not final model or training configurations. For the initial baseline, unsupported characters should raise an error; the inspected validation sample is covered, and coverage should be rechecked when samples change. Keep training and validation stories separate. No model implementation has started.

Update this roadmap after verified milestones. Record changes to scope and the reason for them here; keep the original proposal unchanged. Do not mark a phase complete based on plans or unrun checks.
