FROM python:3.11-slim

# Install essential tools
RUN apt-get update && apt-get install -y \
    git \
    curl \
    bash \
    zsh \
    less \
    vim \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set bash as default shell
SHELL ["/bin/bash", "-c"]

# Create user for non-root development (optional)
ARG USERNAME=dev
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME && \
    useradd -m -s /bin/bash --uid $USER_UID --gid $USER_GID $USERNAME


# Copy and apply the custom bashrc
COPY bashrc /home/${USERNAME}/.bashrc
RUN echo 'if [ -f ~/.bashrc ]; then source ~/.bashrc; fi' >> /home/${USERNAME}/.bash_profile && \
    chown ${USERNAME}:${USERNAME} /home/${USERNAME}/.bashrc /home/${USERNAME}/.bash_profile

# Set workdir
WORKDIR /workspace

# Install Python requirements manager
RUN pip install --upgrade pip setuptools wheel

# Set user
USER ${USERNAME}

# Default to bash shell
CMD [ "bash" ]

# COPY ../.bashrc /home/dev/.bashrc
# RUN chown dev:dev /home/dev/.bashrc
# This line is failing because Docker is trying to copy a file that does not exist at build time — specifically, ../.bashrc relative to the Docker build context.
