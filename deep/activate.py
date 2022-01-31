import numpy as np
import torch
from tqdm import tqdm


def save_checkpoint(epoch, min_val_loss, model_state, opt_state, filename):
    print(f"New minimum reached at epoch #{epoch + 1}, saving model state...")
    checkpoint = {
        "epoch": epoch + 1,
        "min_val_loss": min_val_loss,
        "model_state": model_state,
        "opt_state": opt_state,
    }
    torch.save(checkpoint, "./{}.pt".format(filename))


def load_checkpoint(path, model, optimizer):
    # load check point
    checkpoint = torch.load(path)
    min_val_loss = checkpoint["min_val_loss"]
    model.load_state_dict(checkpoint["model_state"])
    optimizer.load_state_dict(checkpoint["opt_state"])
    return model, optimizer, checkpoint["epoch"], min_val_loss


def training(
    save_name,
    model,
    epochs,
    train_dataloader,
    validation_dataloader,
    BATCH_SIZE,
    optimizer,
    criterion,
    device,
    validate_every=5,
    pretrained=True,
):
    train_losses = []
    validation_losses = []
    min_validation_loss = np.Inf
    if pretrained:
        model, optimizer, _, min_validation_loss = load_checkpoint("./model_state.pt", model, optimizer)

    # Set to train mode
    model.train()

    for epoch in tqdm(range(epochs)):

        # Initialize hidden and cell states with dimension:
        # (num_layers * num_directions, batch, hidden_size)
        states = model.init_hidden_states(BATCH_SIZE)
        running_train_loss = 0.0

        # Begin training
        for idx, (x_batch, y_batch) in enumerate(train_dataloader):
            # Convert to Tensors
            x_batch = x_batch.float().to(device)
            y_batch = y_batch.float().to(device)

            # Truncated Backpropagation
            states = [state.detach() for state in states]

            optimizer.zero_grad()

            # Make prediction
            output, states = model(x_batch, states)

            # Calculate loss
            loss = criterion(output[:, -1, :], y_batch)
            loss.backward()
            running_train_loss += loss.item()

            torch.nn.utils.clip_grad_norm_(model.parameters(), 0.5)
            optimizer.step()

        # Average loss across timesteps
        train_losses.append(running_train_loss / len(train_dataloader))

        if epoch % validate_every == 0:

            # Set to eval mode
            model.eval()

            validation_states = model.init_hidden_states(BATCH_SIZE)
            running_validation_loss = 0.0

            for idx, (x_batch, y_batch) in enumerate(validation_dataloader):

                # Convert to Tensors
                x_batch = x_batch.float().to(device)
                y_batch = y_batch.float().to(device)

                validation_states = [state.detach() for state in validation_states]
                output, validation_states = model(x_batch, validation_states)
                validation_loss = criterion(output[:, -1, :], y_batch)
                running_validation_loss += validation_loss.item()

        validation_losses.append(running_validation_loss / len(validation_dataloader))
        # Reset to training mode
        model.train()

        is_best = running_validation_loss / len(validation_dataloader) < min_validation_loss

        if is_best:
            min_validation_loss = running_validation_loss / len(validation_dataloader)
            save_checkpoint(epoch + 1, min_validation_loss, model.state_dict(), optimizer.state_dict(), save_name)

        """
        # Visualize loss
        epoch_count = range(1, len(training_losses) + 1)
        plt.plot(epoch_count, training_losses, 'r--')
        plt.legend(['Training Loss'])
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.show()

        val_epoch_count = range(1, len(validation_losses) + 1)
        plt.plot(val_epoch_count, validation_losses, 'b--')
        plt.legend(['Validation loss'])
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.show()
        """
