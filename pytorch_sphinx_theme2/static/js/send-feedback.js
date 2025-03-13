// A function to open new issue in GitHub based on {{feedback_url}}.
// Activated when you click the "Send Feedback" button in the footer.
function openGitHubIssue() {
    var baseUrl = document.body.getAttribute('data-feedback-url');
    if (!baseUrl) {
        console.error('Feedback URL not found');
        return;
    }
    var pageUrl = encodeURIComponent(window.location.href);
    var pageTitle = document.querySelector('h1')?.textContent.split('#')[0].trim() || 'Page';
    var issueTitle = encodeURIComponent(`Feedback about ${pageTitle}`);
    var issueBody = encodeURIComponent(`There is the following issue on this page: ${pageUrl}`);
    var labels = encodeURIComponent("module: docs,docs-feedback");
    var feedbackUrl = `${baseUrl}/issues/new?title=${issueTitle}&body=${issueBody}&labels=${labels}`;
    window.open(feedbackUrl, '_blank');
}
