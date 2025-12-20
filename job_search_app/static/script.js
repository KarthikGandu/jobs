// Karthik's Job Search Site - JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Set current year in footer
    document.getElementById('currentYear').textContent = new Date().getFullYear();

    // Search terms management
    const searchTermInput = document.getElementById('searchTermInput');
    const searchTermsTags = document.getElementById('searchTermsTags');
    const expandSection = document.getElementById('expandSection');
    const expandBtn = document.getElementById('expandBtn');
    let searchTerms = [];
    let expandedTerms = [];

    searchTermInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            const term = searchTermInput.value.trim();
            if (term && !searchTerms.includes(term)) {
                searchTerms.push(term);
                addSearchTermTag(term);
                searchTermInput.value = '';
                
                // Show expand button if we have terms
                if (searchTerms.length > 0) {
                    expandSection.style.display = 'block';
                }
            }
        }
    });

    // Auto-expand keywords button - OPTIMIZED for speed
    expandBtn.addEventListener('click', async function() {
        if (searchTerms.length === 0) return;
        
        expandBtn.disabled = true;
        expandBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Expanding (Fast)...';
        
        try {
            const response = await fetch('/api/expand-keywords', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ keywords: searchTerms })
            });
            
            const data = await response.json();
            
            if (data.success) {
                // Clear current terms and add expanded ones (max 15 terms for faster search)
                searchTerms = data.expanded;
                renderSearchTerms();
                
                expandBtn.innerHTML = '<i class="fas fa-check"></i> Expanded to ' + data.count + ' terms!';
                expandBtn.style.background = '#10b981';
                
                // Show helpful message
                const message = document.createElement('div');
                message.style.cssText = 'margin-top: 10px; padding: 10px; background: #d1fae5; border-radius: 8px; color: #065f46; font-size: 0.9rem;';
                message.innerHTML = `✓ Added ${data.count - searchTerms.length} related variations. Click Search to find more jobs!`;
                expandSection.appendChild(message);
                
                setTimeout(() => {
                    message.remove();
                    expandBtn.innerHTML = '<i class="fas fa-magic"></i> Auto-Expand to Related Jobs';
                    expandBtn.style.background = '';
                    expandBtn.disabled = false;
                }, 3000);
            }
        } catch (error) {
            console.error('Error expanding keywords:', error);
            expandBtn.innerHTML = '<i class="fas fa-times"></i> Error';
            expandBtn.disabled = false;
            
            setTimeout(() => {
                expandBtn.innerHTML = '<i class="fas fa-magic"></i> Auto-Expand to Related Jobs';
                expandBtn.disabled = false;
            }, 2000);
        }
    });

    function addSearchTermTag(term) {
        const tag = document.createElement('span');
        tag.className = 'tag';
        tag.innerHTML = `
            ${term}
            <span class="tag-remove" onclick="removeSearchTerm('${term}')">&times;</span>
        `;
        searchTermsTags.appendChild(tag);
    }

    window.removeSearchTerm = function(term) {
        searchTerms = searchTerms.filter(t => t !== term);
        renderSearchTerms();
        
        // Hide expand button if no terms
        if (searchTerms.length === 0) {
            expandSection.style.display = 'none';
        }
    };

    function renderSearchTerms() {
        searchTermsTags.innerHTML = '';
        searchTerms.forEach(term => addSearchTermTag(term));
    }

    // Toggle advanced filters
    const toggleFilters = document.getElementById('toggleFilters');
    const filtersContent = document.getElementById('filtersContent');

    toggleFilters.addEventListener('click', function() {
        filtersContent.classList.toggle('active');
        const icon = toggleFilters.querySelector('i');
        if (filtersContent.classList.contains('active')) {
            icon.style.transform = 'rotate(180deg)';
        } else {
            icon.style.transform = 'rotate(0deg)';
        }
    });

    // Get DOM elements needed for both search and company scraping
    const loadingContainer = document.getElementById('loadingContainer');
    const resultsSection = document.getElementById('resultsSection');
    const loadingText = document.getElementById('loadingText');
    const loadingDetails = document.getElementById('loadingDetails');
    
    // Scrape Companies Button
    const scrapeCompaniesBtn = document.getElementById('scrapeCompaniesBtn');
    const companiesInfo = document.getElementById('companiesInfo');
    
    // Show/hide info on hover
    scrapeCompaniesBtn.addEventListener('mouseenter', function() {
        companiesInfo.style.display = 'block';
    });
    
    scrapeCompaniesBtn.addEventListener('click', async function() {
        // Disable button
        scrapeCompaniesBtn.disabled = true;
        scrapeCompaniesBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Scraping 24 Companies...';
        
        // Show loading
        loadingContainer.style.display = 'block';
        resultsSection.style.display = 'none';
        
        loadingText.textContent = 'Scraping ALL jobs from 24 elite firms...';
        loadingDetails.innerHTML = `
            <p><strong>Firms:</strong> Jane Street, Citadel, HRT, Optiver, Two Sigma, Bridgewater, and 18 more</p>
            <p><strong>This may take 1-2 minutes...</strong></p>
            <p>Getting every open position from each firm's career page</p>
        `;
        
        // Scroll to loading
        loadingContainer.scrollIntoView({ behavior: 'smooth', block: 'center' });
        
        try {
            const startTime = Date.now();
            const response = await fetch('/api/scrape-companies', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({})
            });
            
            const data = await response.json();
            const endTime = Date.now();
            const timeElapsed = ((endTime - startTime) / 1000).toFixed(2);
            
            if (!response.ok) {
                throw new Error(data.error || 'Failed to scrape companies');
            }
            
            // Hide loading, show results
            loadingContainer.style.display = 'none';
            resultsSection.style.display = 'block';
            
            // Update results
            document.getElementById('jobCount').textContent = data.jobs_count;
            
            // Show breakdown by company
            if (data.jobs_by_company) {
                let breakdown = '<div style="margin-top: 10px; font-size: 0.9rem; max-height: 200px; overflow-y: auto;">';
                breakdown += '<strong>Jobs by Company:</strong><br>';
                for (const [company, count] of Object.entries(data.jobs_by_company)) {
                    breakdown += `<span style="display: inline-block; margin: 3px 10px 3px 0;">${company}: ${count}</span>`;
                }
                breakdown += '</div>';
                document.querySelector('.results-header h2').insertAdjacentHTML('afterend', breakdown);
            }
            
            displayJobs(data.jobs);
            
            // Set download URL
            document.getElementById('downloadBtn').onclick = function() {
                window.location.href = data.download_url;
            };
            
            // Success message
            alert(`✓ Successfully scraped ${data.jobs_count} jobs from ${data.companies_scraped} firms in ${timeElapsed} seconds!`);
            
            setTimeout(() => {
                resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }, 100);
            
        } catch (error) {
            console.error('Error:', error);
            loadingContainer.style.display = 'none';
            alert('Error: ' + error.message);
        } finally {
            // Re-enable button
            scrapeCompaniesBtn.disabled = false;
            scrapeCompaniesBtn.innerHTML = '<i class="fas fa-building"></i> Scrape ALL Jobs from 24 Firms <small>Get every open position from Jane Street, Citadel, HRT, Two Sigma, etc.</small>';
        }
    });

    // Form submission
    const jobSearchForm = document.getElementById('jobSearchForm');
    const searchBtn = document.getElementById('searchBtn');

    jobSearchForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        // Validate search terms
        if (searchTerms.length === 0) {
            alert('Please add at least one job title or keyword');
            searchTermInput.focus();
            return;
        }

        // Get selected sites
        const selectedSites = Array.from(document.querySelectorAll('input[name="sites"]:checked'))
            .map(cb => cb.value);

        if (selectedSites.length === 0) {
            alert('Please select at least one job site');
            return;
        }

        // Get form data
        const location = document.getElementById('location').value.trim();
        if (!location) {
            alert('Please enter a location');
            return;
        }

        // Get job types (if selected)
        const jobTypes = Array.from(document.querySelectorAll('input[name="jobType"]:checked'))
            .map(cb => cb.value);

        // Experience level filtering removed - accept all experience levels
        const experienceLevels = [];

        // Get other parameters
        const isRemote = document.getElementById('isRemote').checked;
        const resultsWanted = parseInt(document.getElementById('resultsWanted').value) || 20;
        const distance = parseInt(document.getElementById('distance').value) || 50;
        const hoursOld = document.getElementById('hoursOld').value ? parseInt(document.getElementById('hoursOld').value) : null;

        // Check if companies selected (disabled for now)
        const scrapeCompanies = false;  // Feature disabled
        const scrapeAllCompanies = false;
        
        // Prepare request data
        const requestData = {
            search_terms: searchTerms,
            location: location,
            sites: selectedSites,
            job_types: jobTypes,
            is_remote: isRemote,
            results_wanted: resultsWanted,
            distance: distance,
            hours_old: hoursOld,
            experience_levels: experienceLevels,
            scrape_companies: scrapeCompanies,
            selected_companies: scrapeAllCompanies ? [] : []  // Empty array = scrape all
        };

        // Show loading, hide results
        loadingContainer.style.display = 'block';
        resultsSection.style.display = 'none';
        searchBtn.disabled = true;

        // Update loading text
        loadingText.textContent = 'Searching for jobs...';
        loadingDetails.innerHTML = `
            <p>Sites: ${selectedSites.map(s => s.replace('_', ' ')).join(', ')}</p>
            <p>Search terms: ${searchTerms.join(', ')}</p>
            <p>This may take a moment, please wait...</p>
        `;

        // Scroll to loading
        loadingContainer.scrollIntoView({ behavior: 'smooth', block: 'center' });

        try {
            const startTime = Date.now();
            const response = await fetch('/api/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestData)
            });

            const data = await response.json();
            const endTime = Date.now();
            const timeElapsed = ((endTime - startTime) / 1000).toFixed(2);

            if (!response.ok) {
                throw new Error(data.error || 'Failed to fetch jobs');
            }

            // Hide loading, show results
            loadingContainer.style.display = 'none';
            resultsSection.style.display = 'block';

            // Update results
            document.getElementById('jobCount').textContent = data.jobs_count;
            
            // Show breakdown by search term
            if (data.jobs_by_term) {
                let breakdown = '<div style="margin-top: 10px; font-size: 0.9rem;">';
                for (const [term, count] of Object.entries(data.jobs_by_term)) {
                    breakdown += `<span style="margin-right: 15px;"><strong>${term}:</strong> ${count} jobs</span>`;
                }
                breakdown += '</div>';
                document.querySelector('.results-header h2').insertAdjacentHTML('afterend', breakdown);
            }
            
            displayJobs(data.jobs);

            // Set download URL with dropdown for per-term files
            const downloadBtn = document.getElementById('downloadBtn');
            if (data.download_files && Object.keys(data.download_files).length > 1) {
                // Multiple search terms - show dropdown
                downloadBtn.onclick = function() {
                    showDownloadOptions(data.download_url, data.download_files);
                };
            } else {
                // Single file
                downloadBtn.onclick = function() {
                    window.location.href = data.download_url;
                };
            }

            // Show success message
            loadingDetails.innerHTML = `<p style="color: var(--success-color); font-weight: 600;">✓ Found ${data.jobs_count} jobs in ${timeElapsed} seconds!</p>`;
            setTimeout(() => {
                resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }, 100);

        } catch (error) {
            console.error('Error:', error);
            loadingContainer.style.display = 'none';
            alert('Error: ' + error.message);
        } finally {
            searchBtn.disabled = false;
        }
    });

    // Display jobs
    function displayJobs(jobs) {
        const jobsGrid = document.getElementById('jobsGrid');
        jobsGrid.innerHTML = '';

        if (!jobs || jobs.length === 0) {
            jobsGrid.innerHTML = '<p>No jobs found. Try different search criteria.</p>';
            return;
        }

        jobs.forEach(job => {
            const jobCard = createJobCard(job);
            jobsGrid.appendChild(jobCard);
        });
    }

    // Create job card
    function createJobCard(job) {
        const card = document.createElement('div');
        card.className = 'job-card';

        // Format date
        const datePosted = job.date_posted ? new Date(job.date_posted).toLocaleDateString() : 'N/A';

        // Build job tags
        const tags = [];
        if (job.job_type) tags.push(`<span class="job-tag">${job.job_type}</span>`);
        if (job.is_remote) tags.push(`<span class="job-tag remote"><i class="fas fa-home"></i> Remote</span>`);
        if (job.job_level) tags.push(`<span class="job-tag">${job.job_level}</span>`);

        // Salary info
        let salaryInfo = '';
        if (job.min_amount || job.max_amount) {
            const min = job.min_amount ? `${job.currency || '$'}${formatNumber(job.min_amount)}` : '';
            const max = job.max_amount ? `${job.currency || '$'}${formatNumber(job.max_amount)}` : '';
            salaryInfo = `<div class="job-meta-item"><i class="fas fa-dollar-sign"></i> ${min}${min && max ? ' - ' : ''}${max}${job.interval ? '/' + job.interval : ''}</div>`;
        }

        // Relevance score badge (if available)
        let relevanceBadge = '';
        if (job.relevance_score) {
            const score = (job.relevance_score * 100).toFixed(0);
            const color = score >= 90 ? '#10b981' : score >= 70 ? '#f59e0b' : '#6b7280';
            relevanceBadge = `<span class="relevance-badge" style="background: ${color}; color: white; padding: 3px 8px; border-radius: 12px; font-size: 0.75rem; font-weight: 600;">Match: ${score}%</span>`;
        }

        card.innerHTML = `
            <div class="job-header">
                <div style="flex: 1;">
                    <div class="job-title">
                        <a href="${job.job_url || '#'}" target="_blank" rel="noopener noreferrer">
                            ${job.title || 'Untitled Position'}
                        </a>
                    </div>
                    <div class="job-company">${job.company || 'Company Not Listed'}</div>
                </div>
                <div style="display: flex; gap: 8px; align-items: center;">
                    ${relevanceBadge}
                    <span class="job-site">${(job.site || 'unknown').replace('_', ' ')}</span>
                </div>
            </div>
            
            <div class="job-meta">
                <div class="job-meta-item">
                    <i class="fas fa-map-marker-alt"></i>
                    ${job.location || 'Location not specified'}
                </div>
                <div class="job-meta-item">
                    <i class="fas fa-calendar"></i>
                    ${datePosted}
                </div>
                ${salaryInfo}
            </div>

            ${tags.length > 0 ? `<div class="job-tags">${tags.join('')}</div>` : ''}
        `;

        return card;
    }

    // Helper function to format numbers
    function formatNumber(num) {
        return new Intl.NumberFormat().format(Math.round(num));
    }

    // Show download options for multiple files
    function showDownloadOptions(allUrl, perTermFiles) {
        const modal = document.createElement('div');
        modal.style.cssText = 'position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 9999;';
        
        let options = `<div style="background: white; padding: 30px; border-radius: 15px; max-width: 500px; width: 90%;">
            <h3 style="margin-bottom: 20px; color: #1f2937;">Download Options</h3>
            <div style="margin-bottom: 20px;">
                <button onclick="window.location.href='${allUrl}'; document.body.removeChild(this.closest('div').parentElement)" 
                    style="width: 100%; padding: 12px; margin-bottom: 10px; background: #2563eb; color: white; border: none; border-radius: 8px; font-weight: 600; cursor: pointer;">
                    📦 Download All Jobs Combined
                </button>`;
        
        for (const [term, filename] of Object.entries(perTermFiles)) {
            options += `<button onclick="window.location.href='/api/download/${filename}'; document.body.removeChild(this.closest('div').parentElement)" 
                style="width: 100%; padding: 12px; margin-bottom: 10px; background: #10b981; color: white; border: none; border-radius: 8px; font-weight: 600; cursor: pointer;">
                📄 ${term}
            </button>`;
        }
        
        options += `</div>
            <button onclick="document.body.removeChild(this.parentElement.parentElement)" 
                style="width: 100%; padding: 10px; background: #6b7280; color: white; border: none; border-radius: 8px; cursor: pointer;">
                Cancel
            </button>
        </div>`;
        
        modal.innerHTML = options;
        document.body.appendChild(modal);
    }
    
    window.showDownloadOptions = showDownloadOptions;
});
