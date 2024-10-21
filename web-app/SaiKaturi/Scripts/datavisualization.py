import os
import matplotlib.pyplot as plt
import seaborn as sns

def plot_data(dataset):
    # Path to save images
    image_folder = os.path.expanduser('Images/')

    # Ensure the folder exists
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)

    # Salary Distribution
    plt.figure()  # Create a new figure
    sns.histplot(dataset['avgSalary'], kde=True)
    plt.title('Salary Distribution')
    plt.xlabel('Salary (USD)')
    plt.ylabel('Frequency')
    plt.savefig(os.path.join(image_folder, 'Salary_Distribution.png'))
    plt.close()  # Close the current figure

    # Recency Distribution
    plt.figure()
    sns.histplot(dataset['recency'], kde=True)
    plt.xlabel('Recency in days')
    plt.ylabel('Count of records')
    plt.title('Distribution of Recency Column')
    plt.savefig(os.path.join(image_folder, 'Recency_Distribution.png'))
    plt.close()

    # Job Role Distribution
    plt.figure()
    sns.histplot(dataset['JobRole'], kde=True)
    plt.xlabel('Job Roles')
    plt.ylabel('Count')
    plt.title('Distribution of Job Role Column')
    plt.xticks(rotation=45,ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(image_folder, 'JobRole_Distribution.png'))
    plt.close()

    # Company Score Distribution
    plt.figure()
    sns.histplot(dataset['Company Score'], kde=True)
    plt.xlabel('Company Score')
    plt.ylabel('Count')
    plt.title('Distribution of Company Score Column')
    plt.savefig(os.path.join(image_folder, 'Company_Score.png'))
    plt.close()
