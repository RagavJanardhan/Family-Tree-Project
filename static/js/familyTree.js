// Show the spinner
const spinner = document.getElementById('loading-spinner');
spinner.style.display = 'block';

// Fetch the family tree data and create the visualization
fetch('../family_tree.json')
  .then(res => res.json())
  .then(data => {
    create(data);
    spinner.style.display = 'none'; // Hide the spinner once data is loaded
  })
  .catch(err => {
    console.error(err);
    spinner.style.display = 'none'; // Hide the spinner in case of an error
  });

function calculateAge(birthday, deathDate) {
  if (!birthday || birthday.toLowerCase() === 'unknown') {
    return null;
  }

  // Use Date.UTC to prevent timezone differences
  const birthDate = new Date(birthday); 
  const endDate = deathDate && deathDate.toLowerCase() !== 'alive' ? new Date(deathDate) : new Date();

  let age = endDate.getFullYear() - birthDate.getFullYear();
  const monthDiff = endDate.getMonth() - birthDate.getMonth();

  if (monthDiff < 0 || (monthDiff === 0 && endDate.getDate() < birthDate.getDate())) {
    age--;
  }

  return age;
}

function formatAgeOrAgeAtDeath(birthday, deathDate) {
  const age = calculateAge(birthday, deathDate);

  if (deathDate && deathDate.toLowerCase() !== 'alive') {
    return `Age at Death: ${age} years`;
  } else if (age !== null) {
    return `Age: ${age} years`;
  }

  return 'Age Unknown';
}

function formatBirthDeathDates(birthday, deathDate) {
  if (!birthday || birthday.toLowerCase() === 'unknown') {
    return 'Birthday Unknown';
  }

  const formatDate = dateStr => {
    const date = new Date(dateStr);
    // Use UTC methods to ensure no timezone shift occurs
    const month = (date.getUTCMonth() + 1).toString().padStart(2, '0'); 
    const day = date.getUTCDate().toString().padStart(2, '0');
    const year = date.getUTCFullYear();
    return `${month}/${day}/${year}`;
  };

  if (deathDate && deathDate.toLowerCase() !== 'alive') {
    return `${formatDate(birthday)} - ${formatDate(deathDate)}`;
  }

  return `Birthday: ${formatDate(birthday)}`;
}

function create(data) {
  const container = document.querySelector("#FamilyChart");
  const store = f3.createStore({
    data,
    node_separation: 300,
    level_separation: 150,
  });
  const svg = f3.createSvg(container);

  const Card = f3.elements.Card({
    store,
    svg,
    card_dim: {
      w: 275,
      h: 100,
      text_x: 75,
      text_y: 15,
      img_w: 60,
      img_h: 60,
      img_x: 5,
      img_y: 5,
    },
    card_display: [
      d => `${d.data["first name"]} ${d.data["last name"]}`, // Name
      d => formatAgeOrAgeAtDeath(d.data["birthday"], d.data["death date"]), // Age or Age at Death
      d => formatBirthDeathDates(d.data["birthday"], d.data["death date"]) // Birth and death dates
    ],
    mini_tree: true,
    link_break: false,
  });

  store.setOnUpdate(props => f3.view(store.getTree(), svg, Card, props || {}));
  store.updateTree({ initial: true });
}
