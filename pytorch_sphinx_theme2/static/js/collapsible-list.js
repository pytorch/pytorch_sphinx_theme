/**
 * Collapsible "Subclassed by" list behavior.
 * Finds paragraphs starting with "Subclassed by" that have more than 5 links,
 * collapses them to a single line, and adds a "See All" / "Hide" toggle button.
 */
document.addEventListener('DOMContentLoaded', function() {
    // Find all paragraphs that start with "Subclassed by"
    const paragraphs = document.querySelectorAll('p');

    paragraphs.forEach(function(p) {
        // Check if the paragraph starts with "Subclassed by"
        if (p.textContent.trim().startsWith('Subclassed by')) {
            // Only add toggle if there are many subclasses (more than ~5 links)
            const links = p.querySelectorAll('a');
            if (links.length > 5) {
                // Add the class for styling
                p.classList.add('subclassed-by-list', 'collapsed');

                // Create the toggle button
                const toggle = document.createElement('button');
                toggle.className = 'subclassed-by-toggle';
                toggle.textContent = 'See All (' + links.length + ')';
                toggle.type = 'button';

                // Handle click to expand/collapse
                toggle.addEventListener('click', function(e) {
                    e.preventDefault();

                    if (p.classList.contains('collapsed')) {
                        p.classList.remove('collapsed');
                        p.classList.add('expanded');
                        toggle.textContent = 'Hide';
                    } else {
                        p.classList.remove('expanded');
                        p.classList.add('collapsed');
                        toggle.textContent = 'See All (' + links.length + ')';
                    }
                });

                // Append the toggle to the paragraph
                p.appendChild(toggle);
            }
        }
    });
});
